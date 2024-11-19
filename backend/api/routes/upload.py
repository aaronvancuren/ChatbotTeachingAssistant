from fastapi import APIRouter, File, UploadFile, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
import uuid
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from backend.database.text_processor import process_file, chunk_text
from backend.database.chroma_database import (
    initialize_chromadb,
    get_or_create_collection,
    add_documents,
    update_entry,
    delete_entry,
)

# Initialize templates directory
templates = Jinja2Templates(directory="frontend/templates")

# Initialize ChromaDB client and collection
client = initialize_chromadb()
collection = get_or_create_collection(client, 'file_collection')

upload_router = APIRouter(prefix="/files")

accepted_content_types = [
        'text/plain',
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'text/html',
        'application/rtf'
    ]


@upload_router.get("/upload", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@upload_router.post("/upload")
async def upload_file_api(file: UploadFile = File(...)):
    if file.content_type not in accepted_content_types:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    try:
        content = await file.read()
        chunks = process_file(content, file.filename)

        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to extract text from the file.")

        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"file_name": file.filename, "chunk_index": idx} for idx, _ in enumerate(chunks)]

        # Check if the file already exists in the database
        existing = collection.get(where={"file_name": file.filename})
        if existing['ids']:
            raise HTTPException(status_code=400, detail="File already exists.")

        # Add chunks to the database
        add_documents(collection, chunks, chunk_ids, metadatas)

        return {"message": "File uploaded successfully.", "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

@upload_router.delete("/delete/{file_name}")
async def delete_file_api(file_name: str):
    # Retrieve all entries with the given file_name
    results = collection.get(where={"file_name": file_name})
    if results['ids']:
        # Delete entries from the collection
        collection.delete(ids=results['ids'])
        return {"message": "File deleted successfully.", "file_name": file_name}
    else:
        raise HTTPException(status_code=404, detail="File not found.")

@upload_router.put("/update/{file_name}")
async def update_file_api(
    file_name: str,
    request: Request,
    file: UploadFile = File(None),
    content: str = Form(None)
):

    # Check if the file exists in the database
    existing = collection.get(where={"file_name": file_name})
    if not existing['ids']:
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        if file:
            # Update via file upload
            if file.content_type not in accepted_content_types:
                raise HTTPException(status_code=400, detail="Unsupported file type.")

            # Read the new file content
            new_content = await file.read()
            new_chunks = process_file(new_content, file.filename)

            if not new_chunks:
                raise HTTPException(status_code=400, detail="Failed to extract text from the uploaded file.")
        elif content:
            # Update via form content
            new_chunks = chunk_text(content)
            if not new_chunks:
                raise HTTPException(status_code=400, detail="No content provided for update.")
        else:
            raise HTTPException(status_code=400, detail="No content provided for update.")

        # Generate new chunk IDs and metadatas
        new_chunk_ids = [str(uuid.uuid4()) for _ in new_chunks]
        new_metadatas = [{"file_name": file_name, "chunk_index": idx} for idx, _ in enumerate(new_chunks)]

        # Delete existing entries
        collection.delete(ids=existing['ids'])

        # Add updated chunks to the collection
        add_documents(collection, new_chunks, new_chunk_ids, new_metadatas)

        return JSONResponse(status_code=200, content={"message": "File updated successfully.", "file_name": file_name})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the file: {str(e)}")
    
@upload_router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    # Retrieve all documents from the collection
    documents = collection.get()

    # Extract unique file names from the metadatas
    file_names = set()
    for metadata in documents.get('metadatas', []):
        file_names.add(metadata['file_name'])

    # Pass the list of file names to the template
    return templates.TemplateResponse("upload_index.html", {"request": request, "file_names": file_names})