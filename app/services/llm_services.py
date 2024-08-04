from sqlalchemy import select, insert
from app.database.connector import connect_to_db
from app.database.schemas.llm_message_hist import MessageHistory
from langchain_core.messages import HumanMessage, AIMessage

def parse_output(db_output):
    return [HumanMessage(content=msg) if role == 'human' else AIMessage(content=msg) for msg, role in db_output]

def execute_search_query(stmt, engine):
    with engine.connect() as conn:
        output = conn.execute(stmt)
        results = output.fetchall()
        return results

def get_message_history(limit=None):
    try:
        engine, session = connect_to_db()
        stmt = select(MessageHistory.messages, MessageHistory.role)
        if limit:
            stmt = stmt.limit(limit)
        results = execute_search_query(stmt, engine)
        parsed_results = parse_output(results)
        if results:
            return True, parsed_results
        else:
            return False, None
    except Exception as e:
        print(e)
        return False, None
    finally:
        session.close()

def append_to_history(message, role):
    try:
        engine, session = connect_to_db()
        stmt = insert(MessageHistory).values(
            messages=message,
            role=role
        )
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        session.close()
