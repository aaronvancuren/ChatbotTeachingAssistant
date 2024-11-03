import logging

from databaseConnection import get_db_connection


# Configure logging
logging.basicConfig(level=logging.INFO)


def delete_embedding_by_title(title):
    """
    Deletes a record from the course_materials table based on the title.

    Args:
        title (str): The title of the record to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    # Connect to the database
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    cur = conn.cursor()

    try:
        # Execute the DELETE statement
        # Using parameterized statement to avaoid injection 
        sql_query = """
            DELETE FROM course_materials
            WHERE title = %s;
        """
        cur.execute(sql_query, (title,))
        
        # Check if any rows were affected
        if cur.rowcount == 0:
            logging.warning(f"No record found with title: {title}")
            conn.commit()
            return False
        else:
            logging.info(f"Record with title '{title}' deleted successfully.")
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Error deleting record with title '{title}': {e}")
        conn.rollback()     #Use of rollback is best practice but can be modified based on our needs
        return False
    finally:
        cur.close()
        conn.close()


def delete_embedding_by_id(record_id):
    """
    Deletes a record from the course_materials table based on the id.

    Args:
        record_id (int): The id of the record to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    # Connect to the database
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    cur = conn.cursor()

    try:
        # Execute the DELETE statement
        # Using parameterized statement to avaoid injection 
        sql_query = """
            DELETE FROM course_materials
            WHERE id = %s;
        """
        cur.execute(sql_query, (record_id,))

        # Check if any rows were affected
        if cur.rowcount == 0:
            logging.warning(f"No record found with id: {record_id}")
            conn.commit()
            return False
        else:
            logging.info(f"Record with id '{record_id}' deleted successfully.")
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Error deleting record with id '{record_id}': {e}")      #Use of logging here can be helpful for future debugging and tracking
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()