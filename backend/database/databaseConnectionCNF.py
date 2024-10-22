import psycopg2
from databaseConnection import get_db_connection  # Import the function

# Get the database connection
conn = get_db_connection()
cur = conn.cursor()

# Enables pgvector extension if not already done
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# Creates a table with a vector column
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

# Close the cursor and connection when done
cur.close()
conn.close()