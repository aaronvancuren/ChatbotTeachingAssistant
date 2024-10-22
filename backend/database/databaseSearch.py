import logging
import os

import openai
from openai import OpenAI
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from embeddings_generator import get_embeddings
from databaseConnection import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai = OpenAI()

def search_similar_embeddings(query_text, top_k=5):
    # Compute the query embedding
    query_embedding = get_embeddings(query_text)
    
    if query_embedding is None:
        logging.error("Failed to generate query embedding.")
        return []

    # Ensure the embedding is a fixed-length vector (e.g., length 1536)
    assert len(query_embedding) == 1536, "Embedding size mismatch."

    # Convert the embedding to a list of floats
    query_embedding = [float(x) for x in query_embedding]

    # Connect to the database
    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to connect to the database.")
        return []
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Perform the similarity search
    try:
        # Use parameterized query to prevent SQL injection
        sql_query = """
            SELECT id, title, content
            FROM course_materials
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        cur.execute(sql_query, (query_embedding, top_k))
        results = cur.fetchall()
    except Exception as e:
        logging.error(f"Error during similarity search: {e}")
        results = []
    finally:
        cur.close()
        conn.close()

    return results


