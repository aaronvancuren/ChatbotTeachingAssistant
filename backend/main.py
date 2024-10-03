import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import chromadb
import logging
from typing import List
from text_processor import process_file
from embeddings_generator import get_embeddings, store_embeddings

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the environment variables from .env
load_dotenv()

# Set up default values for OpenAI client
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    organization= os.getenv("OPENAI_ORGANIZATION"),
    project= os.getenv("OPENAI_PROJECT")
)

# Set up FastAPI settings
app = FastAPI()

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGINS")],  # React app runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    """OpenAI message model"""
    content: str

@app.post("/chat/", tags=["Chatbot"])
async def chat(message: Message):
    """OpenAI chat endpoint
    Args:
        message: User chat input
    
    Returns:
        OpenAI response
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message.content
                }
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_MAX_COMPLETION_TOKENS")),
            n=1,
            stop=None,
            temperature=0.7,
            # TODO add user field once user authentication is figured out
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        print(e.status_code)
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        print(e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/upload-files/")
async def upload_files(files: List[UploadFile] = File(...)):
    all_chunks = []
    unsupported_files = []
    stored_ids = []
    for file in files:
        contents = await file.read()
        try:
            chunks = process_file(contents, file.filename)
            if chunks is None:
                unsupported_files.append(file.filename)
                logging.warning(f"Unsupported file type: {file.filename}")
            else:
                all_chunks.extend(chunks)
        except ValueError as e:
            logging.error(f"Error processing file {file.filename}: {e}")
            unsupported_files.append(file.filename)
    
    if all_chunks:
        # Generate embeddings using the updated OpenAI API
        embeddings = get_embeddings(all_chunks)
        # Store embeddings and get stored IDs
        stored_ids = store_embeddings(embeddings, collection_name='teacher_documents')
        logging.info(f"Stored {len(stored_ids)} embeddings in ChromaDB.")
    
    response = {
        "message": "Files processed successfully.",
        "number_of_chunks": len(all_chunks),
        "unsupported_files": unsupported_files,
        "stored_ids": stored_ids if all_chunks else []
    }
    
    return response