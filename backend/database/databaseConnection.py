import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Enables pgvector extension if not already done
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# Creates a table with a vector column (with vector size based on our model chocie)
cur.execute("""
    CREATE TABLE IF NOT EXISTS course_materials (
        id SERIAL PRIMARY KEY,
        title TEXT,
        content TEXT,
        embedding VECTOR(1536)  -- dimension based on our embedding model choice
    );
""")
conn.commit()

print("Table created successfully!")