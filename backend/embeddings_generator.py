# embeddings_generator.py
import os
import openai
import logging
import chromadb

#initialize ChromaDB client
client = chromadb.Client()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embeddings(text_chunks, engine='text-embedding-ada-002', batch_size=16):
    """
    Converts a list of text chunks into embeddings using OpenAI's API.

    Args:
        text_chunks (list): A list of text strings.
        engine (str): The embedding model to use.
        batch_size (int): Number of text chunks to send per API request.

    Returns:
        embeddings (list): A list of embeddings.
    """
    embeddings = []
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        try:
            response = openai.Embedding.create(
                input=batch,
                engine=engine
            )
            for idx, data in enumerate(response['data']):
                embedding = data['embedding']
                embeddings.append({
                    'embedding': embedding,
                    'text': batch[idx]
                })
            logging.info(f"Processed batch {i // batch_size + 1} containing {len(batch)} chunks.")
        except Exception as e:
            logging.error(f"Error processing batch {i // batch_size + 1}: {e}")
            # Handle retries or log the failed batch
            for text in batch:
                embeddings.append({
                    'embedding': None,
                    'text': text,
                    'error': str(e)
                })
    return embeddings

def store_embeddings(embeddings, collection_name='my_collection'):
    """
    Stores embeddings in a ChromaDB collection.

    Args:
        embeddings (list): A list of dictionaries containing embeddings and metadata.
        collection_name (str): The name of the ChromaDB collection.
    """
    collection = client.get_or_create_collection(collection_name)
    for idx, item in enumerate(embeddings):
        if item['embedding'] is not None:
            collection.add(
                embeddings=[item['embedding']],
                metadatas=[{'text': item['text']}],
                ids=[f"{collection_name}_{idx}"]
            )
            logging.info(f"Stored embedding {idx + 1}/{len(embeddings)}")
        else:
            logging.warning(f"Skipping embedding {idx + 1} due to error: {item.get('error')}")