-- initialize_vector_tables.sql
-- SQL script to create tables for storing vector data using pgvector

-- Assuming this script is used after the database is created and pgvector extension is installed

-- Create a table to store documents along with their embeddings
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,  -- The dimensionality matches the OpenAI embedding size
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store queries along with their embeddings for later use
CREATE TABLE IF NOT EXISTS queries (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,  -- The dimensionality matches the OpenAI embedding size
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optionally create an index to speed up nearest neighbor searches on embeddings
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING ivfflat (embedding vector_l2_ops);
CREATE INDEX IF NOT EXISTS idx_queries_embedding ON queries USING ivfflat (embedding vector_l2_ops);
