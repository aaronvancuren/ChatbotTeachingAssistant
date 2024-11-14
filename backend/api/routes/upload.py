from fastapi import APIRouter, File, UploadFile, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
import uuid
from fastapi.responses import HTMLResponse
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
client = initialize_chromadb(True,'backend/chromadb_store')
collection = get_or_create_collection(client, 'file_collection')

upload_router = APIRouter(prefix="/files")

# Dependency to get the current user (if needed)
def get_current_user():
    # Implement your authentication logic here
    pass

# @upload_router.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     documents = collection.get()
#     return templates.TemplateResponse("upload_index.html", {"request": request, "documents": documents})

@upload_router.get("/upload", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@upload_router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    accepted_content_types = [
        'text/plain',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ]

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

        return templates.TemplateResponse("upload_success.html", {"request": request, "filename": file.filename})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

@upload_router.post("/delete/{file_name}")
async def delete_file(request: Request, file_name: str):
    # Retrieve all entries with the given file_name
    results = collection.get(where={"file_name": file_name})
    if results['ids']:
        # Delete entries from the collection
        collection.delete(ids=results['ids'])
        return templates.TemplateResponse("delete_success.html", {"request": request, "file_name": file_name})
    else:
        raise HTTPException(status_code=404, detail="File not found.")

@upload_router.get("/update/{file_name}", response_class=HTMLResponse)
async def get_update_form(request: Request, file_name: str):
    # Retrieve all entries with the given file_name
    results = collection.get(where={"file_name": file_name})
    if results['documents']:
        # Combine chunks into a single string for editing
        document_content = ' '.join(results['documents'])
        return templates.TemplateResponse("update.html", {"request": request, "file_name": file_name, "content": document_content})
    else:
        raise HTTPException(status_code=404, detail="File not found.")

@upload_router.post("/update/{file_name}")
async def update_file(request: Request, file_name: str, content: str = Form(...)):
    # Delete existing entries
    results = collection.get(where={"file_name": file_name})
    if results['ids']:
        collection.delete(ids=results['ids'])
        # Re-process the updated content
        chunks = chunk_text(content)
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"file_name": file_name} for _ in chunks]
        # Add updated chunks to the collection
        add_documents(collection, chunks, chunk_ids, metadatas)
        return templates.TemplateResponse("update_success.html", {"request": request, "file_name": file_name})
    else:
        raise HTTPException(status_code=404, detail="File not found.")
    
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