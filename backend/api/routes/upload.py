import os
from fastapi import APIRouter, Depends, File, UploadFile, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from typing import List
import uuid
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_msal import IDTokenClaims
from fastapi_msal.models import TokenStatus
from backend.api.errors import HTTPError
from backend.api.routes.auth import ACCESS_REQUIRED, get_context, validate_user
from backend.database.text_processor import process_file, chunk_text
from backend.database.chroma_database import (
    initialize_chromadb,
    get_or_create_collection,
    add_documents
)

# Initialize templates directory
templates = Jinja2Templates(directory="frontend/templates")

# Initialize ChromaDB client and collection
client = initialize_chromadb()
collection = get_or_create_collection(client, 'file_collection')

upload_router = APIRouter(prefix="/files")

@upload_router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """
    Renders the main upload page (drag-and-drop UI) and 
    shows a list of already-uploaded file names.
    """
    if (not await validate_user(request, ACCESS_REQUIRED.ADMIN)):
        raise HTTPError(status_code=401, detail="Unauthorized")

    # Retrieve all documents from the collection
    documents = collection.get()

    # Extract unique file names from metadatas
    file_names = set()
    for metadata in documents.get('metadatas', []):
        file_names.add(metadata['file_name'])

    # Pass list of file names into the template
    return templates.TemplateResponse(
        "upload_index.html", 
        {"request": request, "file_names": file_names}
    )

@upload_router.post("/upload")
async def upload_file(request: Request, files: List[UploadFile] = File(...)):
    """
    Accept multiple files at once, process them, 
    and add them to the ChromaDB collection if they do not already exist.
    """
    results = []

    if (not await validate_user(request, ACCESS_REQUIRED.ADMIN)):
        raise HTTPError(status_code=401, detail="Unauthorized")

    for file in files:
        
        try:
                content = await file.read()
                chunks = process_file(content, file.filename)

                if chunks is None:
                    raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

                if not chunks:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Failed to extract text from file: {file.filename}"
                    )

                # Check if this file already exists
                existing = collection.get(where={"file_name": file.filename})
                if existing['ids']:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"File already exists: {file.filename}"
                    )

                # Generate IDs and metadata for each chunk
                chunk_ids = [str(uuid.uuid4()) for _ in chunks]
                metadatas = [
                    {"file_name": file.filename, "chunk_index": idx} 
                    for idx, _ in enumerate(chunks)
                ]

                # Add chunks to the collection
                add_documents(collection, chunks, chunk_ids, metadatas)

                results.append({
                    "filename": file.filename, 
                    "content_type": file.content_type,
                    "message": "File uploaded successfully."
                })
        except HTTPException as he:
            raise he

        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error processing file {file.filename}: {str(e)}"
            )

    return {"uploaded_files": results}

@upload_router.delete("/delete/{file_name}")
async def delete_file(file_name: str, request: Request):
    """
    Deletes all chunks associated with the given file_name.
    """
    if (not await validate_user(request, ACCESS_REQUIRED.ADMIN)):
        raise HTTPError(status_code=401, detail="Unauthorized")

    results = collection.get(where={"file_name": file_name})
    if results['ids']:
        collection.delete(ids=results['ids'])
        return {"message": "File deleted successfully.", "file_name": file_name}
    else:
        raise HTTPException(status_code=404, detail="File not found.")
    
@upload_router.delete("/delete_all")
async def delete_all_files(request: Request):

    if (not await validate_user(request, ACCESS_REQUIRED.ADMIN)):
        raise HTTPError(status_code=401, detail="Unauthorized")

    # Get all documents in the collection
    all_docs = collection.get()
    all_ids = all_docs.get('ids', [])

    if all_ids:
        # Delete all documents
        collection.delete(ids=all_ids)

    return {"message": "All files deleted successfully."}

@upload_router.put("/update/{file_name}")
async def update_file(
    file_name: str,
    request: Request,
    file: UploadFile = File(None),
    content: str = Form(None)
):
    """
    Updates a file by replacing its existing chunks with new ones.
    Can accept either a file or raw text content.
    """
    if (not await validate_user(request, ACCESS_REQUIRED.ADMIN)):
        raise HTTPError(status_code=401, detail="Unauthorized")

    # Check if the file exists in the database
    existing = collection.get(where={"file_name": file_name})
    if not existing['ids']:
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        if file:
            new_content = await file.read()
            new_chunks = process_file(new_content, file.filename)

            if new_chunks is None:
                raise HTTPException(status_code=400, detail="Unsupported file type")

            if not new_chunks:
                raise HTTPException(status_code=400, detail="Failed to extract text from file.")
        elif content:
            new_chunks = chunk_text(content)
            if not new_chunks:
                raise HTTPException(status_code=400, detail="No content provided for update.")
        else:
            raise HTTPException(status_code=400, detail="No content provided for update.")

        # Generate new IDs/metadata
        new_chunk_ids = [str(uuid.uuid4()) for _ in new_chunks]
        new_metadatas = [
            {"file_name": file_name, "chunk_index": idx} 
            for idx, _ in enumerate(new_chunks)
        ]

        # Delete old entries
        collection.delete(ids=existing['ids'])

        # Add updated chunks
        add_documents(collection, new_chunks, new_chunk_ids, new_metadatas)

        return JSONResponse(
            status_code=200, 
            content={"message": "File updated successfully.", "file_name": file_name}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the file: {str(e)}")