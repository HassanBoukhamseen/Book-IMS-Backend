from langchain_core.messages import (
    HumanMessage, 
    AIMessage
)

import sqlite3

conn = sqlite3.connect('message_history.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS message_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    message TEXT NOT NULL
)
''')

conn.commit()
conn.close()

def get_message_history():
    conn = sqlite3.connect('message_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, message FROM message_history')
    history = cursor.fetchall()
    conn.close()
    return [HumanMessage(content=msg) if role == 'human' else AIMessage(content=msg) for role, msg in history]

def append_to_history(role, message):
    conn = sqlite3.connect('message_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO message_history (role, message) VALUES (?, ?)', (role, message))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(get_message_history())
