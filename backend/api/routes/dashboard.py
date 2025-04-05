import uuid

from backend.api.errors import HTTPError
from backend.api.routes import get_context
from backend.database.text_processor import process_file, chunk_text
from backend.database.chroma_database import initialize_chromadb, get_or_create_collection, add_documents
from backend.models import Role, User

from fastapi import APIRouter, Depends, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


class StudentInput(BaseModel):
    email: str

# Initialize templates directory
templates = Jinja2Templates(directory="frontend/templates")

# Initialize ChromaDB client and collection
client = initialize_chromadb()
collection = get_or_create_collection(client, 'file_collection')

page_templates = Jinja2Templates(directory='frontend/templates')

dashboard_router = APIRouter(prefix="/dashboard")

@dashboard_router.get("/")
async def dashboard(request : Request, context: dict = Depends(get_context)):
    """
    Main index page of application
    Args:
        request: the data contained in the request that the server received
        context: the user's token from the current session through Microsoft Authentication
    Returns:
        Index Web Page Response
    """
    user: User = context.get("user")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    return page_templates.TemplateResponse('dashboard.html', {"request": request, "context": context})

@dashboard_router.get("/class")
async def teacher_class_view(request : Request, context: dict = Depends(get_context)):
    user: User = context.get("user")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    # Retrieve all documents from the collection
    documents = collection.get()

    # Extract unique file names from metadatas
    file_names = set()
    for metadata in documents.get('metadatas', []):
        file_names.add(metadata['file_name'])

    # Pass list of file names into the template
    return templates.TemplateResponse("Teacher_ClassView.html", {"request": request, "context": context, "file_names": file_names})

@dashboard_router.post("/upload")
async def upload_file_api(request: Request, files: list[UploadFile] = File(...), context: dict = Depends(get_context)):
    """
    Accept multiple files at once, process them, 
    and add them to the ChromaDB collection if they do not already exist.
    """
    user: User = context.get("user")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    results = []

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

                print(collection.query)
        except HTTPException as he:
            raise he

        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error processing file {file.filename}: {str(e)}"
            )

    return {"uploaded_files": results}

@dashboard_router.delete("/delete/{file_name}")
async def delete_file_api(file_name: str, request: Request, context: dict = Depends(get_context)):
    """
    Deletes all chunks associated with the given file_name.
    """
    user: User = context.get("user")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    results = collection.get(where={"file_name": file_name})
    if results['ids']:
        collection.delete(ids=results['ids'])
        return {"message": "File deleted successfully.", "file_name": file_name}
    else:
        raise HTTPException(status_code=404, detail="File not found.")
    
@dashboard_router.delete("/delete_all")
async def delete_all_files_api(context: dict = Depends(get_context)):
    # Get all documents in the collection
    user: User = context.get("user")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    all_docs = collection.get()
    all_ids = all_docs.get('ids', [])

    if all_ids:
        # Delete all documents
        collection.delete(ids=all_ids)

    return {"message": "All files deleted successfully."}

@dashboard_router.put("/update/{file_name}")
async def update_file_api(
    file_name: str,
    request: Request,
    file: UploadFile = File(None),
    content: str = Form(None),
    context: dict = Depends(get_context)
):
    """
    Updates a file by replacing its existing chunks with new ones.
    Can accept either a file or raw text content.
    """
    user: User = context.get("user")
    if user.role is Role.student:
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
    
@dashboard_router.post("/add_student")
async def add_student(student: StudentInput, request: Request):
    try:
        # Generate a new UUID for the student.
        new_id = uuid.uuid4()
        # Create the student record (or load existing one) using the User object.
        new_user = User(student.email, new_id)
        
        # Now, add the student to a course in the user_courses table.
        # For testing, we'll use the default course id for CS232.
        from backend.models.course import Course
        default_course_id = "e9fb87c0-b500-411b-b1d5-ab581905dc59"
        if not Course.add_student(default_course_id, new_user):
            raise HTTPException(status_code=500, detail="Failed to add student to course.")
        
        return {"success": True, "message": "Student added successfully and enrolled in course."}
    except ValueError as e:
        # Likely means the user record wasn’t found (no invitation) 
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@dashboard_router.post("/add_students_csv")
async def add_students_csv(request: Request, file: UploadFile = File(...)):
    import csv, io, uuid
    from fastapi.responses import JSONResponse
    from fastapi import HTTPException
    from backend.models.user import User
    from backend.models.course import Course
    
    # Use default course id for testing (update as necessary)
    default_course_id = "e9fb87c0-b500-411b-b1d5-ab581905dc59"
    
    try:
        contents = await file.read()
        csv_content = contents.decode("utf-8")
        csv_file = io.StringIO(csv_content)
        reader = csv.reader(csv_file)
        rows = list(reader)
        
        # If first row is a header and contains 'email', skip it
        if rows and "email" in [cell.lower() for cell in rows[0]]:
            data_rows = rows[1:]
        else:
            data_rows = rows
        
        results = []
        for row in data_rows:
            if row:
                email = row[0].strip()
                if email:
                    try:
                        new_uuid = uuid.uuid4()
                        user = User(email, new_uuid)
                        if Course.add_student(default_course_id, user):
                            results.append({"email": email, "success": True, "message": "Student added."})
                        else:
                            results.append({"email": email, "success": False, "message": "Failed to add student to course."})
                    except Exception as e:
                        results.append({"email": email, "success": False, "message": str(e)})
        
        success_count = sum(1 for r in results if r["success"])
        failure_count = len(results) - success_count
        
        return JSONResponse(status_code=200, content={
            "success": True,
            "message": f"Processed CSV: {success_count} added, {failure_count} failed.",
            "details": results
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))