import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import logging

from backend.database.postgre_db_connection import get_db_connection 

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_user(user_id, username, email):
    """
    Inserts a new user into the users table.

    Args:
        user_id (str): The user's unique ID (MS OAuth ID).
        username (str): The user's username.
        email (str): The user's email.

    Returns:
        bool: True if insertion was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        insert_query = """
            INSERT INTO users (id, username, email)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        cur.execute(insert_query, (user_id, username, email))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error inserting user: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()


def get_user_by_id(user_id):
    """
    Retrieves a user from the users table by ID.

    Args:
        user_id (str): The user's unique ID.

    Returns:
        dict or None: User data if found, else None.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT * FROM users WHERE id = %s;"
        cur.execute(select_query, (user_id,))
        user = cur.fetchone()
        return user
    
    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def update_user_email(user_id, new_email):
    """
    Updates a user's email in the users table.

    Args:
        user_id (str): The user's unique ID.
        new_email (str): The new email address.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        update_query = "UPDATE users SET email = %s WHERE id = %s;"
        cur.execute(update_query, (new_email, user_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating user email: {e}")
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
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

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

def get_role_by_name(role_name):
    """
    Retrieves a role from the roles table by name.

    Args:
        role_name (str): The name of the role.

    Returns:
        dict or None: Role data if found, else None.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT * FROM roles WHERE role_name = %s;"
        cur.execute(select_query, (role_name,))
        role = cur.fetchone()
        return role
    
    except Exception as e:
        logging.error(f"Error retrieving role: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def create_class_section(classname, class_catalog, section, professor_id, teaching_assistant_id):
    """
    Inserts a new class section into the class_sections table.

    Args:
        classname (str): Name of the class.
        class_catalog (str): Catalog of the class.
        section (int): Section number.
        professor_id (str): ID of the professor.
        teaching_assistant_id (str): ID of the teaching assistant.

    Returns:
        int or None: ID of the newly created class section, or None if failed.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur = conn.cursor()

    try:
        insert_query = """
            INSERT INTO class_sections (classname, class_catalog, section, professor_id, teaching_assistant_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (classname, class_catalog, section, professor_id, teaching_assistant_id))
        class_section_id = cur.fetchone()[0]
        conn.commit()
        return class_section_id
    
    except Exception as e:
        logging.error(f"Error creating class section: {e}")
        conn.rollback()
        return None
    
    finally:
        cur.close()
        conn.close()

def get_class_section_by_id(class_section_id):
    """
    Retrieves a class section by ID.

    Args:
        class_section_id (int): The ID of the class section.

    Returns:
        dict or None: Class section data if found, else None.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT * FROM class_sections WHERE id = %s;"
        cur.execute(select_query, (class_section_id,))
        class_section = cur.fetchone()
        return class_section
    
    except Exception as e:
        logging.error(f"Error retrieving class section: {e}")
        return None
    
    finally:
        cur.close()
        conn.close()

def update_class_section_professor(class_section_id, new_professor_id):
    """
    Updates the professor of a class section.

    Args:
        class_section_id (int): The ID of the class section.
        new_professor_id (str): The new professor's user ID.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        update_query = "UPDATE class_sections SET professor_id = %s WHERE id = %s;"
        cur.execute(update_query, (new_professor_id, class_section_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating class section professor: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def delete_class_section(class_section_id):
    """
    Deletes a class section.

    Args:
        class_section_id (int): The ID of the class section.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        delete_query = "DELETE FROM class_sections WHERE id = %s;"
        cur.execute(delete_query, (class_section_id,))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error deleting class section: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def assign_role_to_user_in_class(user_id, class_section_id, role_id):
    """
    Assigns a role to a user in a class section.

    Args:
        user_id (str): The user's unique ID.
        class_section_id (int): The ID of the class section.
        role_id (int): The ID of the role.

    Returns:
        bool: True if assignment was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        insert_query = """
            INSERT INTO user_class_roles (user_id, class_section_id, role_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, class_section_id) DO UPDATE SET role_id = %s;
        """
        cur.execute(insert_query, (user_id, class_section_id, role_id, role_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error assigning role: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def get_user_roles_in_class(user_id, class_section_id):
    """
    Retrieves the roles assigned to a user in a class section.

    Args:
        user_id (str): The user's unique ID.
        class_section_id (int): The ID of the class section.

    Returns:
        list: A list of role names assigned to the user in the class.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    
    cur = conn.cursor()

    try:
        select_query = """
            SELECT r.role_name
            FROM user_class_roles ucr
            JOIN roles r ON ucr.role_id = r.id
            WHERE ucr.user_id = %s AND ucr.class_section_id = %s;
        """
        cur.execute(select_query, (user_id, class_section_id))
        roles = [row[0] for row in cur.fetchall()]
        return roles
    
    except Exception as e:
        logging.error(f"Error retrieving user roles: {e}")
        return []
    
    finally:
        cur.close()
        conn.close()

def remove_role_from_user_in_class(user_id, class_section_id):
    """
    Removes a user's role in a class section.

    Args:
        user_id (str): The user's unique ID.
        class_section_id (int): The ID of the class section.

    Returns:
        bool: True if removal was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        delete_query = "DELETE FROM user_class_roles WHERE user_id = %s AND class_section_id = %s;"
        cur.execute(delete_query, (user_id, class_section_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error removing role: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def create_conversation(class_section_id, user_id, summary_name=None):
    """
    Creates a new conversation.

    Args:
        class_section_id (int): The ID of the class section.
        user_id (str): The user's unique ID.
        summary_name (str): Optional summary name for the conversation.

    Returns:
        int or None: The ID of the new conversation, or None if failed.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur = conn.cursor()

    try:
        insert_query = """
            INSERT INTO conversations (class_section_id, user_id, summary_name)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (class_section_id, user_id, summary_name))
        conversation_id = cur.fetchone()[0]
        conn.commit()
        return conversation_id
    
    except Exception as e:
        logging.error(f"Error creating conversation: {e}")
        conn.rollback()
        return None
    
    finally:
        cur.close()
        conn.close()

def get_conversations_by_user(user_id):
    """
    Retrieves all conversations for a given user.

    Args:
        user_id (str): The user's unique ID.

    Returns:
        list: A list of conversations.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = "SELECT * FROM conversations WHERE user_id = %s;"
        cur.execute(select_query, (user_id,))
        conversations = cur.fetchall()
        return conversations
    
    except Exception as e:
        logging.error(f"Error retrieving conversations: {e}")
        return []
    
    finally:
        cur.close()
        conn.close()

def update_conversation_summary(conversation_id, new_summary_name):
    """
    Updates the summary name of a conversation.

    Args:
        conversation_id (int): The ID of the conversation.
        new_summary_name (str): The new summary name.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        update_query = "UPDATE conversations SET summary_name = %s WHERE id = %s;"
        cur.execute(update_query, (new_summary_name, conversation_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating conversation summary: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def delete_conversation(conversation_id):
    """
    Deletes a conversation and its associated messages.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        delete_query = "DELETE FROM conversations WHERE id = %s;"
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

def add_message(conversation_id, msg_role, content):
    """
    Adds a message to a conversation.

    Args:
        conversation_id (int): The ID of the conversation.
        msg_role (str): The role of the message sender ('system', 'user', or 'assistant').
        content (str): The message content.

    Returns:
        int or None: The ID of the new message, or None if failed.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return None
    
    cur = conn.cursor()

    try:
        insert_query = """
            INSERT INTO messages (conversation_id, msg_role, content)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (conversation_id, msg_role, content))
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

def get_messages_in_conversation(conversation_id):
    """
    Retrieves all messages in a conversation.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        list: A list of messages.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        select_query = """
            SELECT * FROM messages WHERE conversation_id = %s ORDER BY id ASC;
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

def update_message_content(message_id, new_content):
    """
    Updates the content of a message.

    Args:
        message_id (int): The ID of the message.
        new_content (str): The new message content.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        update_query = "UPDATE messages SET content = %s WHERE id = %s;"
        cur.execute(update_query, (new_content, message_id))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error updating message content: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def delete_message(message_id):
    """
    Deletes a message.

    Args:
        message_id (int): The ID of the message.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn = get_db_connection()

    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    
    cur = conn.cursor()

    try:
        delete_query = "DELETE FROM messages WHERE id = %s;"
        cur.execute(delete_query, (message_id,))
        conn.commit()
        return True
    
    except Exception as e:
        logging.error(f"Error deleting message: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

