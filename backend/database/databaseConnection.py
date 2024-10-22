import psycopg2
import os
from dotenv import load_dotenv

def get_db_connection():

    # Load environment variables from .env file
    load_dotenv()

    # Database connection configuration
    db_config = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", 5432)
    }
    db_config["port"] = int(db_config["port"])  # Ensure port is integer

    # Connect to PostgreSQL using psycopg2
    conn = psycopg2.connect(**db_config)
    return conn