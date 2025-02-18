#!/usr/bin/env python3
import psycopg2
import argparse
import logging
import os
import re
from psycopg2.extensions import connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG to see each statement being executed
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the relative path to the SQL script folder
SCRIPT_DIR = os.path.dirname(__file__)

# Define the script execution order
CREATE_DATABASE_SCRIPT = "create_database.sql"
DROP_DATABASE_SCRIPT = "drop_database.sql"

CREATE_SCRIPTS = [
    "create_type_course_subject.sql",
    "create_type_role.sql",
    "create_table_users.sql",
    "create_table_courses.sql",
    "create_table_user_courses.sql",
    "create_table_user_conversations.sql",
    "create_table_messages.sql",
]

def parse_sql_statements(sql_script):
    """
    Splits an SQL script into individual statements.
    This simple parser splits on semicolons (;) that are not inside a quoted string.
    
    Note: For more complex scripts (with PL/pgSQL functions, dollar quoting, etc.)
    consider using a dedicated SQL parser.
    """
    # Remove single-line comments (-- comment)
    sql_script = re.sub(r'--.*', '', sql_script)

    # Remove multi-line comments (/* comment */)
    sql_script = re.sub(r'/\*.*?\*/', '', sql_script, flags=re.DOTALL)
    
    statements = []
    statement = ""
    in_quote = False
    quote_char = None

    for char in sql_script:
        # Check for start or end of a quoted string
        if char in ("'", '"'):
            if not in_quote:
                in_quote = True
                quote_char = char
            elif quote_char == char:
                in_quote = False
                quote_char = None

        # If we hit a semicolon outside of quotes, it marks the end of a statement
        if char == ';' and not in_quote:
            if statement.strip():
                statements.append(statement.strip())
            statement = ""
        else:
            statement += char

    # Catch any trailing statement that may not have ended with a semicolon.
    if statement.strip():
        statements.append(statement.strip())
    
    return statements

def run_sql_script(conn: connection, script_name: str):
    """
    Reads an SQL script from the database folder, splits it into individual statements,
    and executes them using the given database connection.
    """
    script_path = os.path.join(SCRIPT_DIR, script_name)

    if not os.path.exists(script_path):
        logger.error("File does not exist: %s", script_path)
        raise FileNotFoundError(f"File {script_path} does not exist.")

    with open(script_path, 'r') as file:
        sql_script = file.read()

    statements = parse_sql_statements(sql_script)
    logger.debug("Parsed %d statements from %s", len(statements), script_name)
    with conn.cursor() as cur:
        statement: str
        for statement in statements:
            if statement.strip():
                logger.debug("Executing statement: %s", statement)
                cur.execute(statement)
    logger.info("Successfully executed script: %s", script_name)

def database_exists(host, port, user, password, dbname):
    try:
        with psycopg2.connect(
            host=host,
            port=port,
            dbname="postgres",
            user=user,
            password=password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}';")
                return cur.fetchone() is not None
    except Exception as e:
        logger.error(f"Error checking database existence: {e}")
        return False
    finally:
        conn.close()

def recreate_database(host, port, user, password, dbname):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname="postgres",
            user=user,
            password=password,
        )
        conn.autocommit = True
        
        if(database_exists(host, port, user, password, dbname)):
            run_sql_script(conn, DROP_DATABASE_SCRIPT)
            logger.info(f"Database '{dbname}' dropped successfully.")
        
        run_sql_script(conn, CREATE_DATABASE_SCRIPT)
        logger.info(f"Database '{dbname}' created successfully.")
    except Exception as e:
        logger.error(f"Error recreating database: {e}")
        exit(1)
    finally:
        conn.close()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run SQL scripts to drop and re-create PostgreSQL tables in dependency order."
    )
    parser.add_argument('--host', default='localhost', help='Database host (default: localhost)')
    parser.add_argument('--port', type=int, default=5432, help='Database port (default: 5432)')
    parser.add_argument('--dbname', default='chatbot', help='Name of the database (default: chatbot)')
    parser.add_argument('--user', default='teaching-assistant', help='Database user (default: teaching-assistant)')
    parser.add_argument('--password', required=True, help='Database password')
    return parser.parse_args()

def main():
    args = parse_args()
    recreate_database(args.host, args.port, args.user, args.password, args.dbname)

    try:
        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            dbname=args.dbname,
            user=args.user,
            password=args.password
        )

        # Ensure we control transactions (disable autocommit)
        conn.autocommit = False
        
        logger.info(
            "Connected to database %s at %s:%s as user %s",
            args.dbname, args.host, args.port, args.user
        )
    except Exception as e:
        logger.error("Error connecting to database: %s", e)
        return 1

    try:
        # Run all create scripts in order.
        for create_script in CREATE_SCRIPTS:
            logger.info("Running create script: %s", create_script)
            run_sql_script(conn, create_script)

        # If all scripts executed successfully, commit the transaction.
        conn.commit()
        logger.info("All scripts executed successfully. Transaction committed.")

    except Exception as e:
        conn.rollback()
        logger.error("Error executing scripts. Transaction rolled back: %s", e)
        return 1

    finally:
        conn.close()
        logger.info("Database connection closed.")

    return 0

if __name__ == '__main__':
    exit(main())