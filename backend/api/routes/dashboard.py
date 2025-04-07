import uuid

from backend.api.errors import HTTPError
from backend.api.routes import get_context
from backend.database.text_processor import process_file, chunk_text
from backend.database.chroma_database import initialize_chromadb, get_or_create_collection, add_documents
from backend.models import Role, User
from backend.database.postgres import read_user_by_email, create_user
from fastapi import APIRouter, Depends, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates



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
    # if user.role is Role.student:
    #     raise HTTPError(status_code=401, detail="Unauthorized")
    
    return page_templates.TemplateResponse('dashboard.html', {"request": request, "context": context})

@dashboard_router.get("/class")
async def teacher_class_view(request : Request, context: dict = Depends(get_context)):
    user: User = context.get("user")
    # if user.role is Role.student:
    #     raise HTTPError(status_code=401, detail="Unauthorized")

    from backend.models.course import Course
    
    # course = None
    # students = []

    # class_list = context.get("class_list", [])
    # if class_list:
        # Assume the first item in class_list is a dict with an 'id' key
        # This is just until get courses functionality is done
        # first_class = class_list[0]
        # course = Course()
        # course.id = first_class['id']
        # students = course.get_students()

    # course = Course()
    # course.id = "e9fb87c0-b500-411b-b1d5-ab581905dc59"  # Hard-coded test course UUID

     # Construct the Course with its ID right in the constructor
    course = Course(
    id="e9fb87c0-b500-411b-b1d5-ab581905dc59",
    instructor_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    display_name="CS232 - Introduction to Computer Science",
    subject=13,
    course_number="232",
    section_number="1",
    title="Introduction to CS",
    model="default_model",
    prompt="Default course prompt for CS232",
    documents_path="/path/to/cs232/documents",
    image_path="/path/to/cs232/image",
    students=[]
)
    students = course.get_students()


    students = []
    if course is not None:
        students = course.get_students()

    
    # Retrieve all documents from the collection
    documents = collection.get()

    # Extract unique file names from metadatas
    file_names = set()
    for metadata in documents.get('metadatas', []):
        file_names.add(metadata['file_name'])

    # Pass list of file names into the template
    return templates.TemplateResponse("Teacher_ClassView.html", {"request": request, "context": context, "file_names": file_names, "students": students})

@dashboard_router.post("/upload")
async def upload_file_api(request: Request, files: list[UploadFile] = File(...), context: dict = Depends(get_context)):
    """
    Accept multiple files at once, process them, 
    and add them to the ChromaDB collection if they do not already exist.
    """
    user: User = context.get("user")
    # if user.role is Role.student:
    #     raise HTTPError(status_code=401, detail="Unauthorized")
    
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
    # if user.role is Role.student:
    #     raise HTTPError(status_code=401, detail="Unauthorized")
    
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
    # if user.role is Role.student:
    #     raise HTTPError(status_code=401, detail="Unauthorized")
    
    all_docs = collection.get()
    all_ids = all_docs.get('ids', [])

    if all_ids:
        # Delete all documents
        collection.delete(ids=all_ids)

    return {"message": "All files deleted successfully."}

@dashboard_router.post("/add_student")
async def add_student(request: Request):
    from backend.database.postgres import read_user_by_email, create_user, create_user_course, read_users_for_course
    from fastapi import HTTPException

    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email must be provided")

    user_record = read_user_by_email(email)
    if user_record is None:
        # Create a new student record if needed
        if not create_user(email, email, 'student'):
            raise HTTPException(status_code=500, detail="Failed to create student")
        user_record = read_user_by_email(email)
        if user_record is None:
            raise HTTPException(status_code=500, detail="Student record not found after creation")

    student_id = user_record.id  # <-- use attribute access
    default_course_id = "e9fb87c0-b500-411b-b1d5-ab581905dc59"
    
    # Attempt to enroll the student
    success = create_user_course(default_course_id, str(student_id))
    if not success:
        enrolled_users = read_users_for_course(default_course_id)
        if str(student_id) not in enrolled_users:
            raise HTTPException(status_code=500, detail="Failed to enroll student in course")

    return {"success": True, "message": "Student added successfully and enrolled in course."}

@dashboard_router.delete("/remove_student")
async def remove_student(request: Request):
    from fastapi import HTTPException
    from backend.database.postgres import (
        read_user_by_email,
        delete_user_course,
        read_users_for_course,
    )

    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email must be provided")

    # Get the user record to find their ID
    user_record = read_user_by_email(email)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")

    student_id = user_record.id
    default_course_id = "e9fb87c0-b500-411b-b1d5-ab581905dc59"  # Or whichever course

    # Attempt to remove the student from the specified course
    success = delete_user_course(default_course_id, str(student_id))
    if not success:
        # Double check whether the user is still enrolled
        enrolled_users = read_users_for_course(default_course_id)
        if str(student_id) in enrolled_users:
            raise HTTPException(
                status_code=500,
                detail="Failed to remove student from course."
            )

    return {"success": True, "message": "Student removed from course."}