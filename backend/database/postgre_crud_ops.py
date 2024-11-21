from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values
from psycopg2.extras import RealDictCursor
import logging
import textwrap

from backend.database.embeddings_generator import get_embeddings
from backend.database.databaseConnection import get_db_connection 

embedding_vector_length = 1536

# Configure logging
logging.basicConfig(level=logging.INFO)

def insert_embeddings_into_db(text_chunks):
    """
    Generates embeddings for given text chunks and inserts them into the database.

    Args:
        text_chunks (list): List of text strings to generate embeddings for.

    Returns:
        list: A list of IDs of the inserted records.
    """
    # Generate embeddings
    embeddings = get_embeddings(text_chunks)
    logging.info("Embeddings generated successfully.")

    # Connect to PostgreSQL
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return
    cur = conn.cursor()

    inserted_ids = []

    # Prepare data for insertion
    records_to_insert = []
    for idx, item in enumerate(embeddings):
        title = f"Insert {idx + 1}"  # Title based on enumerated inserts
        content = item['text']       # Plain text of the text chunk that produced the embedding
        embedding = item['embedding']

        if embedding is not None:
            # Ensure the embedding is a fixed-length vector (e.g., length 1536)
            assert len(embedding) == embedding_vector_length, "Embedding size mismatch."

            # Convert the embedding to a PostgreSQL array string
            embedding_str = "{" + ",".join(map(str, embedding)) + "}"

            records_to_insert.append((title, content, AsIs(f"'{embedding_str}'::vector")))
        else:
            logging.error(f"Failed to get embedding for: {title}")

    if not records_to_insert:
        logging.error("No embeddings to insert into the database.")
        cur.close()
        conn.close()
        return

    try:
        # Use execute_values for batch insertion
        insert_query = """
            INSERT INTO course_materials (title, content, embedding)
            VALUES %s
            RETURNING id;
        """

        # Execute batch insertion
        execute_values(
            cur,
            insert_query,
            records_to_insert,
            template="(%s, %s, %s)"
        )

        # Fetch all the assigned ids
        ids = cur.fetchall()
        inserted_ids.extend([id_tuple[0] for id_tuple in ids])
        logging.info(f"{len(inserted_ids)} records inserted successfully.")

        # Commit the transaction
        conn.commit()
    except Exception as e:
        logging.error(f"Database insertion error: {e}")
        conn.rollback()
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        logging.info("Database connection closed.")

    return inserted_ids  # Return the list of inserted ids


def search_similar_embeddings(query_text, top_k=5):
    """
    Searches for embeddings similar to the query text.

    Args:
        query_text (str): The query text.
        top_k (int): The number of top similar records to return.

    Returns:
        list: A list of dictionaries containing 'id', 'title', and 'content' of similar records.
    """
    # Compute the query embedding
    query_embedding_result = get_embeddings([query_text])
    if not query_embedding_result or query_embedding_result[0]['embedding'] is None:
        logging.error("Failed to generate query embedding.")
        return []

    # Extract the embedding from the result
    query_embedding = query_embedding_result[0]['embedding']

    # Ensure the embedding is a fixed-length vector
    assert len(query_embedding) == embedding_vector_length, "Embedding size mismatch."

    # Convert the embedding to a PostgreSQL array string
    embedding_str = "{" + ",".join(map(str, query_embedding)) + "}"

    # Connect to the database
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Perform the similarity search
    try:
        # Use parameterized query with AsIs to prevent SQL injection
        sql_query = """
            SELECT id, title, content
            FROM course_materials
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        cur.execute(sql_query, (AsIs(f"'{embedding_str}'"), top_k))
        results = cur.fetchall()
    except Exception as e:
        logging.error(f"Error during similarity search: {e}")
        results = []
    finally:
        cur.close()
        conn.close()

    return results


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
        sql_query = textwrap.dedent("""
            DELETE FROM course_materials
            WHERE title = %s;
        """)
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
        sql_query = textwrap.dedent("""
            DELETE FROM course_materials
            WHERE id = %s;
        """)
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