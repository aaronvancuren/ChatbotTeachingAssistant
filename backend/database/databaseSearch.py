import logging
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import AsIs

from backend.database.embeddings_generator import get_embeddings
from backend.database.databaseConnection import get_db_connection

embedding_vector_length = 1536 

# Configure logging
logging.basicConfig(level=logging.INFO)

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