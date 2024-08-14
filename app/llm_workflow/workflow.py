from typing import Optional, TypedDict
from langgraph.graph import StateGraph, END
from app.llm_workflow.llm_utils import (
    INTENT_SYSTEM_PROMPT, 
    GREETING_SYSTEM_PROMPT,
    RECOMMENDATION_SYSTEM_PROMPT,
    CHAT_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    ADD_BOOK_SYSTEM_PROMPT,
    parse_db_output
)
from app.llm_workflow.llm import chain
from app.llm_workflow.vector_store import base_retriever
from langchain_core.messages import (
    SystemMessage, 
    HumanMessage, 
)
from app.services.llm_services import get_message_history, append_to_history
from app.database.schemas.books import Book
from app.database.connector import connect_to_db

class StateSchema(TypedDict):
    response: Optional[str]
    query: Optional[str]
    intent: Optional[str]

workflow = StateGraph(StateSchema)

def get_intent_node(state):
    query = state.get('query', '').strip()
    success, history = get_message_history(limit=None)
    if not success:
        history = []
    model_input = {
        "system_message": [SystemMessage(content=INTENT_SYSTEM_PROMPT)],
        "human_messages": history + [HumanMessage(content=query)]
    }
    output = chain.invoke(model_input)
    append_to_history(query, 'human')
    append_to_history(output, 'ai')
    return {"intent": output}

def greeting_node(state):
    query = state.get('query', '').strip()
    success, history = get_message_history(limit=None)
    if not success:
        history = []
    model_input = {
        "system_message": [SystemMessage(content=GREETING_SYSTEM_PROMPT)],
        "human_messages": history + [HumanMessage(content=query)]
    }
    output = chain.invoke(model_input)
    append_to_history(query, 'human')
    append_to_history(output, 'ai')
    return {"response": output}

def book_recommendation_node(state):
    query = state.get('query', '').strip()
    query_with_context = query + f" Here is some context. Choose ONLY from the following books {parse_db_output(base_retriever.invoke(query))}"
    print("*"*50)
    print(parse_db_output(base_retriever.invoke(query)))
    print("*"*50)
    success, history = get_message_history(limit=None)
    if not success:
        history = []
    model_input = {
        "system_message": [SystemMessage(content=RECOMMENDATION_SYSTEM_PROMPT)],
        "human_messages": history + [HumanMessage(content=query_with_context)]
    }
    output = chain.invoke(model_input)
    append_to_history(query_with_context, 'human')
    append_to_history(output, 'ai')
    return {"response": output}

def book_chat_node(state):
    query = state.get('query', '').strip()
    success, history = get_message_history(limit=None)
    if not success:
        history = []
    model_input = {
        "system_message": [SystemMessage(content=CHAT_SYSTEM_PROMPT)],
        "human_messages": history + [HumanMessage(content=query)]
    }
    output = chain.invoke(model_input)
    append_to_history(query, 'human')
    append_to_history(output, 'ai')
    return {"response": output}

def book_summary_node(state):
    query = state.get('query', '').strip()
    success, history = get_message_history(limit=None)
    if not success:
        history = []
    model_input = {
        "system_message": [SystemMessage(content=SUMMARY_SYSTEM_PROMPT)],
        "human_messages": history + [HumanMessage(content=query)]
    }
    output = chain.invoke(model_input)
    append_to_history(query, 'human')
    append_to_history(output, 'ai')
    return {"response": output}

def insert_book_in_db(book: dict):
    to_add = Book(
        book_id=str(book["book_id"]),
        title=book["title"], 
        subtitle=book["subtitle"],
        thumbnail="Unknown",
        author_name=book["authors"],
        genre=book["categories"], 
        description=book["description"], 
        year=book["published_year"], 
        rating=book["average_rating"],
        num_pages=book["num_pages"],
        ratings_count=book["ratings_count"]   
    )
    engine, session = connect_to_db()
    try:
        session.add(to_add)
        session.commit()
        book_id = to_add.book_id
        return True, "Book added Successfully", book_id
    except Exception as e:
        session.rollback()
        return False, e, None
    finally:
        session.close()

def add_book_node(state):
    query = state.get('query', '').strip()
    success, history = get_message_history(limit=None)
    if not success:
        history = []
    model_input = {
        "system_message": [SystemMessage(content=ADD_BOOK_SYSTEM_PROMPT)],
        "human_messages": history + [HumanMessage(content=query)]
    }
    output = chain.invoke(model_input)
    try:
        book = eval(output)
        print(book)
        success, message, book_id = insert_book_in_db(book)
        if not success:
            print(message)
        else:
            print("Added new book with ID:", book_id)
    except Exception as e:
        print(e)

    append_to_history(query, 'human')
    append_to_history(output, 'ai')
    return {"response": output}

def node_transition(state):
    intent = state.get('intent', '')
    if "greeting" in intent:
        return "handle_greeting"
    elif "chat" in intent:
        return "book_chat"
    elif "summarize" in intent:
        return "book_summary"
    elif "book recommendations" in intent:
        return "book_recommendation"
    elif "add book" in intent:
        return "add_book"
    else:
        return "get_intent"

workflow.add_node("get_intent", get_intent_node)
workflow.add_node("handle_greeting", greeting_node)
workflow.add_node("add_book", add_book_node)
workflow.add_node("book_recommendation", book_recommendation_node)
workflow.add_node("book_summary", book_summary_node)
workflow.add_node("book_chat", book_chat_node)

workflow.add_conditional_edges(
    "get_intent",
    node_transition
)


workflow.set_entry_point("get_intent")
workflow.add_edge("handle_greeting", END)
workflow.add_edge("add_book", END)
workflow.add_edge("book_recommendation", END)
workflow.add_edge("book_summary", END)
workflow.add_edge("book_chat", END)

assistant = workflow.compile()

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        inputs = {"query": user_input}
        for event in assistant.stream(inputs, stream_mode="values"):
            if event.get('response', '') != '':
                print("*"*50)
                print(f"Intent: {event['intent']}")
                print("*"*50)
                print(f"AI: {event['response']}")
