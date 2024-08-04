from typing import Optional, TypedDict
from langgraph.graph import StateGraph, END
from app.llm_workflow.llm_utils import (
    INTENT_SYSTEM_PROMPT, 
    GREETING_SYSTEM_PROMPT,
    RECOMMENDATION_SYSTEM_PROMPT,
    parse_db_output
)
from app.llm_workflow.llm import chain
from app.llm_workflow.vector_store import base_retriever
from langchain_core.messages import (
    SystemMessage, 
    HumanMessage, 
)
from app.services.llm_services import get_message_history, append_to_history


class StateSchema(TypedDict):
    response: Optional[str]
    query: Optional[str]
    intent: Optional[str]

workflow = StateGraph(StateSchema)

def get_intent_node(state):
    query = state.get('query', '').strip()
    success, history = get_message_history()
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
    success, history = get_message_history()
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
    query_with_context = query + f" Here is some context: {parse_db_output(base_retriever.invoke(query))}"
    success, history = get_message_history()
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

def add_book_node(state):
    response = "Not implemented yet"
    append_to_history(response, 'ai')
    return {"response": response}

def node_transition(state):
    intent = state.get('intent', '')
    if "greeting" in intent:
        return "handle_greeting"
    elif "book recommendation" in intent:
        return 'book_recommendation'
    elif "add book" in intent:
        return "add_book"
    else:
        return "get_intent"

workflow.add_node("get_intent", get_intent_node)
workflow.add_node("handle_greeting", greeting_node)
workflow.add_node("book_recommendation", book_recommendation_node)
workflow.add_node("add_book", add_book_node)

workflow.add_conditional_edges(
    "get_intent",
    node_transition
)

workflow.set_entry_point("get_intent")
workflow.add_edge("handle_greeting", END)
workflow.add_edge("book_recommendation", END)
workflow.add_edge("add_book", END)

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
