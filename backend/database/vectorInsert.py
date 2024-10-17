import openai
from openai import OpenAI
import os
import psycopg2
import logging
from dotenv import load_dotenv
from embeddings_generator import get_embeddings

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai = OpenAI()


# Database connection configuration
db_config = {
     "dbname": os.getenv("DB_NAME"),        # Database name from .env file
    "user": os.getenv("DB_USER"),          # PostgreSQL username from .env file
    "password": os.getenv("DB_PASSWORD"),  # PostgreSQL password from .env file
    "host": os.getenv("DB_HOST", "localhost"),  # PostgreSQL host, default to 'localhost'
    "port": os.getenv("DB_PORT", 5432)     # PostgreSQL port, default to 5432
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