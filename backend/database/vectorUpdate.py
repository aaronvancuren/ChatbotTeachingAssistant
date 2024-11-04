import logging
from psycopg2.extensions import AsIs

from backend.database.embeddings_generator import get_embeddings
from backend.database.databaseConnection import get_db_connection

embedding_vector_length = 1536 

def update_embedding_by_id(record_id, new_content):
    """
    Updates the content and embedding of a record in the course_materials table based on the id.

    Args:
        record_id (int): The id of the record to update.
        new_content (str): The new content to update.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Generate the new embedding
    new_embedding = get_embeddings([new_content])
    if not new_embedding or new_embedding[0]['embedding'] is None:
        logging.error("Failed to generate new embedding.")
        return False
    
    # Extract the embedding from the result
    new_embedding = new_embedding[0]['embedding']

    # Ensure the embedding is a fixed-length vector (e.g., length 1536)
    assert len(new_embedding) == embedding_vector_length, "Embedding size mismatch."

    # Convert the embedding to a PostgreSQL array string
    embedding_str = "{" + ",".join(map(str, new_embedding)) + "}"

    # Connect to the database
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    cur = conn.cursor()

    try:
        # Execute the UPDATE statement with proper casting
        sql_query = """
            UPDATE course_materials
            SET content = %s, embedding = %s::vector
            WHERE id = %s;
        """
        cur.execute(sql_query, (new_content, AsIs(embedding_str), record_id))

        # Check if any rows were affected
        if cur.rowcount == 0:
            logging.warning(f"No record found with id: {record_id}")
            conn.commit()
            return False
        else:
            logging.info(f"Record with id '{record_id}' updated successfully.")
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Error updating record with id '{record_id}': {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
    

def update_embedding_by_title(title, new_content):
    """
    Updates the content and embedding of a record in the course_materials table based on the title.

    Args:
        title (str): The title of the record to update.
        new_content (str): The new content to update.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Generate the new embedding
    new_embedding = get_embeddings([new_content])
    if not new_embedding or new_embedding[0]['embedding'] is None:
        logging.error("Failed to generate new embedding.")
        return False
    
    # Extract the embedding from the result
    new_embedding = new_embedding[0]['embedding']

    # Ensure the embedding is a fixed-length vector (e.g., length 1536)
    assert len(new_embedding) == embedding_vector_length, "Embedding size mismatch."

    # Convert the embedding to a PostgreSQL array string
    embedding_str = "{" + ",".join(map(str, new_embedding)) + "}"

    # Connect to the database
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return False
    cur = conn.cursor()

    try:
        # Execute the UPDATE statement with proper casting
        sql_query = """
            UPDATE course_materials
            SET content = %s, embedding = %s::vector
            WHERE title = %s;
        """
        cur.execute(sql_query, (new_content, AsIs(embedding_str), title))

        # Check if any rows were affected
        if cur.rowcount == 0:
            logging.warning(f"No record found with title: {title}")
            conn.commit()
            return False
        else:
            logging.info(f"Record with title '{title}' updated successfully.")
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Error updating record with title '{title}': {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()