import chromadb
from chromadb import Documents, Embeddings
from openai import OpenAI
from typing import List, Dict
import logging
import os

openai = OpenAI()

# Function to generate embeddings using OpenAI's API
def generate_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model=os.getenv("OPENAI_EMBEDDING_MODEL")
    )
    embedding = response.data[0].embedding
    return embedding

# Function to initialize ChromaDB client with optional persistent storage
def initialize_chromadb(use_persistence=False, persist_directory=None):
    if use_persistence and persist_directory:
        client = chromadb.PersistentClient(path=persist_directory)
        logging.info(f"ChromaDB initialized with persistent storage at '{persist_directory}'.")
    else:
        # Initialize without persistence
        client = chromadb.Client()
        logging.info("ChromaDB initialized without persistent storage.")
    return client

# Function to get or create a collection
def get_or_create_collection(client, collection_name):
    collection = client.get_or_create_collection(name=collection_name)
    return collection

# Function to add documents to the collection
def add_documents(collection, documents, ids, metadatas):
    embeddings = [generate_embedding(doc) for doc in documents]
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

# Function to retrieve entries based on file name
def retrieve_by_file_name(collection, file_name):
    results = collection.get(
        where={'file_name': file_name}
    )
    return results

# Function to update an existing entry
def update_entry(collection, id, updated_document=None, updated_metadata=None):
    update_params = {'ids': [id]}
    if updated_document:
        update_params['documents'] = [updated_document]
        update_params['embeddings'] = [generate_embedding(updated_document)]
    if updated_metadata:
        update_params['metadatas'] = [updated_metadata]
    collection.update(**update_params)

# Function to delete an entry
def delete_entry(collection, id):
    collection.delete(ids=[id])

def nearest_neighbor_search(collection, input_text: str, n_results: int = 5) -> List[Dict]:
    """
    Performs a nearest neighbor search on the collection based on the input_text.
    
    Args:
        input_text (str): The query text to search against the collection.
        n_results (int): Number of top results to return.
    
    Returns:
        List[Dict]: A list of dictionaries containing 'content', 'metadata', and 'distance'.
    """
    try:
        input_embedding = generate_embedding(input_text)
        results = collection.query(
            query_embeddings=[input_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        relevant_documents = []
        for doc, meta, distance in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
            relevant_documents.append({
                'content': doc,
                'metadata': meta,
                'distance': distance
            })
        
        logging.info(f"Retrieved {len(relevant_documents)} relevant documents for the query.")

        return relevant_documents
    except Exception as e:
        logging.error(f"Error during nearest neighbor search: {e}")
        return []