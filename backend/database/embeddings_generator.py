#ChatGPT was used to help write this code
import logging
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set OpenAI API key
openai = OpenAI()

def get_embeddings(text_chunks, model='text-embedding-ada-002', batch_size=16):
    """
    Converts a list of text chunks into embeddings using OpenAI's API.

    Args:
        text_chunks (list): A list of text strings.
        model (str): The embedding model to use.
        batch_size (int): Number of text chunks to send per API request.

    Returns:
        embeddings (list): A list of embeddings.
    """
    embeddings = []
    total_batches = (len(text_chunks) - 1) // batch_size + 1
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        try:
            response = openai.embeddings.create(
                input=batch,
                model=model
            )
            for idx, data in enumerate(response.data):
                embedding = data.embedding
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