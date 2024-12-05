-- initialize_database.sql
-- SQL script to create the database

-- Connect to the default postgres database
\c postgres;

-- Drop the existing chatbot_teaching_assistant database if it exists
DROP DATABASE IF EXISTS chatbot_teaching_assistant;

-- Create a new chatbot_teaching_assistant database
CREATE DATABASE chatbot_teaching_assistant;

-- Connect to the newly created chatbot_teaching_assistant database
\c chatbot_teaching_assistant;

-- Note: The '\c' command is a psql meta-command used to connect to a specific database.