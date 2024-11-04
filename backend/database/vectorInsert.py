from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values
import logging

from backend.database.embeddings_generator import get_embeddings
from backend.database.databaseConnection import get_db_connection  # Import the function

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