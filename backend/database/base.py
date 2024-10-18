import psycopg2

connection = psycopg2.connect()

def initialize_conversation(user_id: int, message: str="Hello, how can I help you?"):
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute('INSERT INTO conversations (user_id) VALUES (%s) RETURNING id', (user_id,))
            conversation_id = curs.fetchone()[0]
            conn.commit()
            conversation = get_conversation(conversation_id)
            return conversation_id, conversation

def get_conversation(conversation_id: int):
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute('SELECT role, content FROM messages WHERE conversation_id = %s ORDER BY id', (conversation_id))
            return [{'role': row[0], 'content': row[1]} for row in curs.fetchall()]

def save_message(user_id: int, conversation_id: int, role: str, content: str):
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute('INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s)', (conversation_id, role, content))
            conn.commit()

connection.close()