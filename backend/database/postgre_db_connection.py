import psycopg2
import os

def get_db_connection():
    # Retrieve required environment variables
    dbname = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
    port = int(os.getenv('DB_PORT', 5432))    # Default to 5432 if not set

    # Database connection configuration
    db_config = {
        "dbname": dbname,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }

    # Connect to PostgreSQL using psycopg2
    conn = psycopg2.connect(**db_config)
    return conn