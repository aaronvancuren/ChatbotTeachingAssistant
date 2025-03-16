import logging
import os
import uuid

import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor, RealDictRow

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_db_connection():
    # Retrieve required environment variables
    dbname = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
    port = int(os.getenv('DB_PORT', 5432))    # Default to 5432 if not set

    # Database connection configuration
    db_config = {
        "dbname": dbname,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }

    # Connect to PostgreSQL using psycopg2
    conn = psycopg2.connect(**db_config)
    return conn

def create_user(display_name, email, role='student'):
    """
    Inserts a new user into the users table.

    Args:
        display_name (str): The user's display name.
        email (str): The user's email (must be unique).
        role (str): The user's role (defaults to 'student').

    Returns:
        bool: True if insertion was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO users (display_name, email, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        cur.execute(insert_query, (display_name, email, role))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error inserting user: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def read_user_by_id(user_id):
    """
    Retrieves a user from the users table by ID.

    Args:
        user_id (str): The user's unique ID.

    Returns:
        str or None: User data if found, else None.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT display_name, role FROM users WHERE id = %s;"
        cur.execute(select_query, (user_id,))
        row = cur.fetchone()
        
        if row is None:
            return None
        
        return row
    
    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def read_user_by_email(email) -> RealDictRow:
    """
    Retrieves a user from the users table by email.

    Args:
        email (str): The user's email.

    Returns:
        str or None: User's display name if found, else None.
        str or None: User's role if found, else None.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT id, display_name, email, role FROM users WHERE email = %s;"
        cur.execute(select_query, (email))
        row: RealDictRow = cur.fetchone()

        if row is None:
            return None
        
        return row
    
    except Exception as e:
        logging.error(f"Error retrieving user by email: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def read_email_by_id(user_id):
    """
    Retrieves the email of a user from the users table by their ID.

    Args:
        user_id (str): The user's unique ID (UUID).

    Returns:
        str or None: The user's email if found, else None.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None

    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT email FROM users WHERE id = %s;"
        cur.execute(select_query, (user_id,))
        row = cur.fetchone()

        if row is None:
            return None

        return row['email']

    except Exception as e:
        logging.error(f"Error retrieving user email by ID: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def update_user_display_name(display_name, email):
    """
    Updates a user's display name in the users table based on their display name.

    Args:
        display_name (str): The user's display name.
        new_email (str): The new email address.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        update_query = "UPDATE users SET display_name = %s WHERE email = %s;"
        cur.execute(update_query, (display_name, email))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating user display name: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def set_user_id(id: uuid, email: str):
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()
    
    try:
        update_query = "UPDATE users SET id = %s WHERE email = %s;"
        cur.execute(update_query, (id, email))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error updating user display name: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def delete_user(user_id):
    """
    Deletes a user from the users table.

    Args:
        user_id (str): The user's unique ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        delete_query = "DELETE FROM users WHERE id = %s;"
        cur.execute(delete_query, (user_id,))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def create_course(instructor_id, display_name, subject, course_number, section_number, title, model, prompt, documents_path, image_path):
    """
    Inserts a new course into the courses table.

    Args:
        instructor_id (str): The instructors unique user ID (UUID).
        display_name (str): The display name of the course (e.g., 'Intro to Chemistry').
        subject (str): The subject of the course (type course_subject in DB).
        course_number (int): The numeric course number (e.g., 101).
        section_number (int): The numeric section number (e.g., 1).
        title (str): The descriptive title of the course (e.g., 'Chemistry Basics').
        model (str): The model type for the course (type model in DB).
        prompt (str): The prompt text (optional).
        documents_path (str): The path where documents for this course are stored.
        image_path (str): The path to an image or logo representing this course.

    Returns:
        str or None: The UUID of the newly created course, or None if failed.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur: cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO courses (instructor_id, display_name, subject, course_number, section_number, title, model, prompt, documents_path, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (instructor_id, display_name, subject, course_number, section_number, title, model, prompt, documents_path, image_path))
        course_id = cur.fetchone()[0]
        conn.commit()
        return course_id
    
    except Exception as e:
        logging.error(f"Error creating course: {e}")
        conn.rollback()
        return None
    
    finally:
        cur.close()
        conn.close()

def read_course_by_id(course_id):
    """
    Retrieves a course by ID.

    Args:
        course_id (str): The ID of the course.

    Returns:
        dict or None: Course data if found, else None.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT * FROM courses WHERE id = %s;"
        cur.execute(select_query, (course_id,))
        class_section = cur.fetchone()
        return class_section
    
    except Exception as e:
        logging.error(f"Error retrieving course info: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def update_course_title(course_id, new_title):
    """
    Updates the title of a course.

    Args:
        course_id (str): The ID of the course.
        new_title (str): The new course title.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        update_query = "UPDATE courses SET title = %s WHERE id = %s;"
        cur.execute(update_query, (new_title, course_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating course title: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()
    
def update_course_model(course_id, new_model):
    """
    Updates the model of a course.

    Args:
        course_id (str): The ID of the course.
        new_model (str): The new model name.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        update_query = "UPDATE courses SET model = %s WHERE id = %s;"
        cur.execute(update_query, (new_model, course_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating course model: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def delete_course(course_id):
    """
    Deletes a course from the course table.

    Args:
        class_section_id (str): The ID of the course.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        delete_query = "DELETE FROM courses WHERE id = %s;"
        cur.execute(delete_query, (course_id,))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error deleting course: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def create_user_conversation(course_id, user_id, title):
    """
    Creates a new conversation.

    Args:
        course_id (str): The ID of the course.
        user_id (str): The user's unique ID.
        title (str): Title for the conversation.

    Returns:
        str or None: The ID of the new conversation, or None if failed.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur: cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO user_conversations (course_id, user_id, title)
            VALUES (%s, %s, %s)
            RETURNING conversation_id;
        """
        cur.execute(insert_query, (course_id, user_id, title))
        conversation_id = cur.fetchone()[0]
        conn.commit()
        return conversation_id
    
    except Exception as e:
        logging.error(f"Error creating user conversation: {e}")
        conn.rollback()
        return None
    
    finally:
        cur.close()
        conn.close()

def read_conversations_by_user(user_id, course_id):
    """
    Retrieves all conversations IDs for a given user.

    Args:
        user_id (str): The user's unique ID.
        course_id (str): The course's unique ID.

    Returns:
        list: A list of conversations IDs.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    
    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT conversation_id FROM user_conversations WHERE user_id = %s AND course_id = %s;"
        cur.execute(select_query, (user_id, course_id))
        rows = cur.fetchall()

        conversation_ids = [row['conversation_id'] for row in rows]
        return conversation_ids
    
    except Exception as e:
        logging.error(f"Error retrieving conversation ids: {e}")
        return []
    
    finally:
        cur.close()
        conn.close()

def update_conversation_title(conversation_id, new_title):
    """
    Updates the title of a conversation.

    Args:
        conversation_id (str): The ID of the conversation.
        new_title (str): The new title name.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        update_query = "UPDATE user_conversations SET title = %s WHERE conversation_id = %s;"
        cur.execute(update_query, (new_title, conversation_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating conversation title: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def delete_conversation(conversation_id):
    """
    Deletes a conversation from the user_conversation table.

    Args:
        conversation_id (str): The ID of the conversation.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        delete_query = "DELETE FROM user_conversations WHERE conversation_id = %s;"
        cur.execute(delete_query, (conversation_id,))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error deleting conversation: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def create_message(conversation_id, prompt, response):
    """
    Adds a message to the messages table.

    Args:
        conversation_id (str): The ID of the conversation.
        prompt (str): The prompt given in the conversation.
        response (str): The response given in the conversation.

    Returns:
        str or None: The ID of the new message, or None if failed.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur: cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO messages (conversation_id, prompt, response)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (conversation_id, prompt, response))
        message_id = cur.fetchone()[0]
        conn.commit()
        return message_id
    
    except Exception as e:
        logging.error(f"Error adding message: {e}")
        conn.rollback()
        return None
    
    finally:
        cur.close()
        conn.close()

def read_messages_from_conversation(conversation_id):
    """
    Retrieves all messages for a conversation.

    Args:
        conversation_id (str): The ID of the conversation.

    Returns:
        list: A list of prompts and responses for a conversation.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    
    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = """
            SELECT prompt, response FROM messages WHERE conversation_id = %s ORDER BY id ASC;
        """
        cur.execute(select_query, (conversation_id,))
        messages = cur.fetchall()
        return messages
    
    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return []
    
    finally:
        cur.close()
        conn.close()

def create_user_course(course_id, user_id):
    """
    Creates a new user course.

    Args:
        course_id (str): The ID of the course.
        user_id (str): The user's unique ID.

    Returns:
        bool: True if creation was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur: cursor = conn.cursor()

    try:
        insert_query = """
            INSERT INTO user_courses (course_id, user_id)
            VALUES (%s, %s)
            ON CONFLICT (course_id, user_id) DO NOTHING
        """
        cur.execute(insert_query, (course_id, user_id))
        inserted = (cur.rowcount == 1)
        conn.commit()
        return inserted
    
    except Exception as e:
        logging.error(f"Error creating user course: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def read_users_for_course(course_id):
    """
    Retrieves all user IDs associated with a given course.

    Args:
        course_id (str): The UUID of the course.

    Returns:
        list: A list of user IDs (UUID strings) for users linked to the specified course.
        If no records are found or an error occurs, an empty list is returned.
    """

    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return []

    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        select_query = """
            SELECT user_id FROM user_courses WHERE course_id = %s;
        """
        cur.execute(select_query, (course_id,))
        rows = cur.fetchall()

        user_ids = [row['user_id'] for row in rows]
        return user_ids
    
    except Exception as e:
        logging.error(f"Error retrieving users for course {course_id}: {e}")
        return []
    
    finally:
        cur.close()
        conn.close()

def delete_user_course(course_id, user_id):
    """
    Deletes a user-course from the user_courses table.

    Args:
        course_id (str): The UUID of the course.
        user_id (str): The UUID of the user.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """

    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False

    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        delete_query = """
            DELETE FROM user_courses WHERE course_id = %s AND user_id = %s;
        """
        cur.execute(delete_query, (course_id, user_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error deleting user course: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def delete_user_courses_by_course(course_id):
    """
    Deletes all user-course associations from the user_courses table for a given course.

    Args:
        course_id (str): The UUID of the course.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    conn: connection = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False

    cur: cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        delete_query = """
            DELETE FROM user_courses WHERE course_id = %s;
        """
        cur.execute(delete_query, (course_id,))
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"Error deleting user courses by course_id '{course_id}': {e}")
        conn.rollback()
        return False

    finally:
        cur.close()
        conn.close()