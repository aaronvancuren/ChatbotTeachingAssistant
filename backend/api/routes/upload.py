from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from backend.core.templates import page_templates
from typing import List
from backend.database import text_processor, embeddings_generator
import logging

upload_router = APIRouter()

# The File Upload Page
@upload_router.get("/upload")
async def upload_file_page(request: Request):
    """
    File Upload page of the application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Upload Web Page Response
    """
    return page_templates.TemplateResponse('file_upload.html', {"request": request})

# Endpoint to handle file processing
@upload_router.post("/process")
async def process_files(files: List[UploadFile] = File(...)):
    """
    Handle file upload and processing using text_processor and embeddings_generator.
    """
    try:
        response_data = []

        for file in files:
            file_bytes = await file.read()
            chunks = text_processor.process_file(file_bytes, file.filename)

            if not chunks:
                raise HTTPException(status_code=400, detail=f"Failed to process file: {file.filename}")

            embeddings = embeddings_generator.get_embeddings(chunks)

            response_data.append({
                "filename": file.filename,
                "num_chunks": len(chunks),
                "extracted_text": chunks,
                "embeddings": embeddings,
            })

        return response_data
    except Exception as e:
        logging.error(f"Error processing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))