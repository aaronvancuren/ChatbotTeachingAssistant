-- initialize_tables.sql
-- SQL script to create traditional relational tables for chatbot interactions

-- Create a table to store user information
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,  --MS OAuth ID
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Create a table to store roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- Insert predefined roles into the roles table
INSERT INTO roles (role_name)
VALUES ('Professor'), ('Student'), ('TeachingAssistant'), ('Admin')
ON CONFLICT (role_name) DO NOTHING;

-- Create a table to store class sections
CREATE TABLE IF NOT EXISTS class_sections (
    id SERIAL PRIMARY KEY,                   -- GUUID
    classname VARCHAR(255) NOT NULL,          -- Name of the class
    class_catalog VARCHAR(50) NOT NULL,       -- Catalog of class
    section INTEGER NOT NULL,                 -- Section of class
    professor_id VARCHAR(255) REFERENCES users(id),
    teaching_assistant_id VARCHAR(255) REFERENCES users(id)
);

-- Create a join table to store user roles in class sections
CREATE TABLE IF NOT EXISTS user_class_roles (
    user_id VARCHAR(255) REFERENCES users(id),
    class_section_id INTEGER REFERENCES class_sections(id),
    role_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (user_id, class_section_id)
);

-- Create a table to store conversation history
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    class_section_id INTEGER REFERENCES class_sections(id),
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    summary_name VARCHAR(255)
);

-- Create a table to store individual messages within a conversation
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    msg_role VARCHAR(10) NOT NULL,  -- 'system', 'user', or 'assistant' to distinguish participants
    content TEXT NOT NULL
);