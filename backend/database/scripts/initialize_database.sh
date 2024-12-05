#!/bin/bash

# Function to find the .env file within the main project directory
find_env_file() {
    project_dir="$(dirname "$0")/../../"
    if [ -f "$project_dir/.env" ]; then
        echo "$project_dir/.env"
    else
        echo "Error: .env file not found in the expected directory: $project_dir"
        return 1
    fi
}

# Load environment variables from the found .env file
ENV_FILE=$(find_env_file)
if [ -n "$ENV_FILE" ]; then
    echo "Failed to find the .env file. Please ensure it exists in the expected project directory." >&2
    exit 1
fi
export $(grep -v '^#' "$ENV_FILE" | xargs -d '\n')

initialize_database() {
    # Check if the SQL file for database initialization exists
    if [ -f "$(dirname "$0")/initialize_database.sql" ]; then
        if PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -f "$(dirname "$0")/initialize_database.sql"; then
            echo "Database initialized successfully from initialize_database.sql."
        else
            echo "Failed database initialized from initialize_database.sql." >&2
            exit 1
        fi
    else
        echo "initialize_database.sql file not found in the expected directory." >&2
        exit 1
    fi
}

initialize_tables() {
    # Check if the SQL file for creating traditional tables exists
    if [ -f "$(dirname "$0")/initialize_tables.sql" ]; then
        PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -f "$(dirname "$0")/initialize_tables.sql"
        echo "Traditional tables initialized successfully from initialize_tables.sql."
    else
        echo "initialize_tables.sql file not found in the expected directory." >&2
        exit 1
    fi
}

# Initialize the database and apply extensions
initialize_database

# Initialize traditional tables
initialize_tables