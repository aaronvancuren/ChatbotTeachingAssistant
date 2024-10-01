# DB Directory

The `database/` directory manages database connections, sessions, and initialization. It includes modules responsible for setting up the database engine, creating sessions, and initializing database tables.

## **Contents**

- **`session.py`**: Configures the database session maker and provides functions to get database sessions.
- **`base.py`**: Contains the base class for all ORM models and handles the creation of database tables.
- **`__init__.py`**: Initializes the `database` package and can include database initialization logic.

## **Purpose**

- Manages the database engine and connections.
- Provides session management for database transactions.
- Initializes and maintains the database schema.