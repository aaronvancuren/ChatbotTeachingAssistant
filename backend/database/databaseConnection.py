import psycopg2

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