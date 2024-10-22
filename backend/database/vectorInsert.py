import openai
from openai import OpenAI
import os
import psycopg2
import logging
from dotenv import load_dotenv
from embeddings_generator import get_embeddings
from databaseConnection import get_db_connection  # Import the function

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai = OpenAI()

def insert_embeddings_into_db(text_chunks):
    """
    Generates embeddings for given text chunks and inserts them into the database.

    Args:
        text_chunks (list): List of text strings to generate embeddings for.
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

    # Insert embeddings into the database
    for idx, item in enumerate(embeddings):
        title = f"Insert {idx + 1}"  # Title based on enumerated inserts
        content = item['text']       # Plain text of the text chunk that produced the embedding
        embedding = item['embedding']

        if embedding is not None:
            try:
                # Insert into database
                cur.execute("""
                    INSERT INTO course_materials (title, content, embedding)
                    VALUES (%s, %s, %s)
                """, (title, content, embedding))
            except psycopg2.Error as e:
                logging.error(f"Database insertion error for {title}: {e}")
        else:
            logging.error(f"Failed to get embedding for: {title}")

    # Commit the transaction and close the connection
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Embeddings inserted into the database successfully.")