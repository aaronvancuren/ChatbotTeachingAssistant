import openai
from openai import OpenAI
import psycopg2
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set OpenAI API key
load_dotenv()
openai = OpenAI()

#Using Carter's emedding method
def get_embeddings(text_chunks, model='text-embedding-ada-002', batch_size=16):
    """
    Converts a list of text chunks into embeddings using OpenAI's API.

    Args:
        text_chunks (list): A list of text strings.
        model (str): The embedding model to use.
        batch_size (int): Number of text chunks to send per API request.

    Returns:
        embeddings (list): A list of embeddings.
    """
    embeddings = []
    total_batches = (len(text_chunks) - 1) // batch_size + 1
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        try:
            response = openai.embeddings.create(
                input=batch,
                model=model
            )
            for idx, data in enumerate(response.data):
                embedding = data.embedding
                embeddings.append({
                    'embedding': embedding,
                    'text': batch[idx]
                })
            logging.info(f"Processed batch {i // batch_size + 1} containing {len(batch)} chunks.")
        except Exception as e:
            logging.error(f"Error processing batch {i // batch_size + 1}: {e}")
            # Handle retries or log the failed batch
            for text in batch:
                embeddings.append({
                    'embedding': None,
                    'text': text,
                    'error': str(e)
                })
    return embeddings

# Database connection configuration
db_config = {
    "dbname": "my_vector_db",  # Your database name
    "user": "my_user",         # Your PostgreSQL username
    "password": "my_password", # Your PostgreSQL password
    "host": "localhost",       # Or any other host where PostgreSQL is running
    "port": 5432               # Default port for PostgreSQL
}

# Connect to PostgreSQL using psycopg2
conn = psycopg2.connect(**db_config)
cur = conn.cursor()

#
#We can add test files or scripts here to test the get_emedding function
#
test_text_chunks = [
    "Introduction to C and Unix",
    "C is a very powerful low-level programming langauage",
    "Unix is a powerful operating system designed for flexibility and security"
]

embeddings = get_embeddings(test_text_chunks)

# Insert embeddings into the database
for idx, item in enumerate(embeddings):
    title = f"Test Insert: {idx + 1}"  #Title for enumerated test inserts
    content = item['text']  # plain text that produced the embeddings 
    embedding = item['embedding']
    
    if embedding is not None:
        # Insert into database
        cur.execute("""
            INSERT INTO course_materials (title, content, embedding)
            VALUES (%s, %s, %s)
        """, (title, content, embedding))
    else:
        logging.error(f"Failed to get embedding for: {title}")

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()