import psycopg2

connection = psycopg2.connect()

def initialize_conversation(user_id):
    with connection as conn:
        with conn.cursor() as curs:
            message = "Hello, how can I help you?"
            conversation_id = 1
            curs.execute("", user_id, conversation_id, message)
            return curs.fetchone()

def get_conversation(user_id, conversation_id):
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute("")
            return curs.fetchall()

def save_message(user_id, conversation_id, role, content):
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute("")
            conn.commit()

connection.close()