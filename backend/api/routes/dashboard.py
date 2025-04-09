import uuid
import csv, io
from backend.api.errors import HTTPError
from backend.api.routes import get_context
from backend.database.text_processor import process_file, chunk_text
from backend.database.chroma_database import initialize_chromadb, get_or_create_collection, add_documents
from backend.models.course import Course
from backend.models import Role, User
from backend.models.subject import Subject
from fastapi import APIRouter, Depends, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from backend.database.postgres import (
    read_user_by_email,
    create_user,
    create_user_course,
    delete_user_course,
    read_users_for_course,
    delete_all_user_courses,
)


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

    if user is None:
        raise HTTPError(status_code=401, detail="Unauthorized")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    return page_templates.TemplateResponse('dashboard.html', {"request": request, "context": context})

@dashboard_router.get("/class")
async def teacher_class_view(request: Request, context: dict = Depends(get_context)):
    user: User = context.get("user")
    if user is None:
        raise HTTPError(status_code=401, detail="Unauthorized")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    # The courses list is retrieved from the context
    courses = context.get("courses", [])
    if not courses:
        raise HTTPError(status_code=404, detail="No courses found for this user.")

    # Get the course_id from the query parameters
    course_id = request.query_params.get("course_id")
    
    if course_id:
        # Attempt to find a matching Course object in context["courses"]
        selected_course = next((c for c in courses if str(c.id) == course_id), None)
        if not selected_course:
            raise HTTPError(status_code=404, detail="Course not found in context.")
    else:
        # If no course_id is provided
        raise HTTPError(status_code=404, detail="No courses found for this user.")
    
    # Add the selected course ID into the context for template usage
    context.update({"selected_course_id": selected_course.id})
    
    students = selected_course.get_students()
    
    documents = collection.get()
    file_names = {metadata['file_name'] for metadata in documents.get('metadatas', [])}
    
    return templates.TemplateResponse("Teacher_ClassView.html",{"request": request, "context": context, "file_names": file_names, "students": students}
    )

@dashboard_router.post("/upload")
async def upload_file_api(request: Request, files: list[UploadFile] = File(...), context: dict = Depends(get_context)):
    """
    Accept multiple files at once, process them, 
    and add them to the ChromaDB collection if they do not already exist.
    """
    user: User = context.get("user")
    if user is None:
        raise HTTPError(status_code=401, detail="Unauthorized")
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
    if user is None:
        raise HTTPError(status_code=401, detail="Unauthorized")
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
    if user is None:
        raise HTTPError(status_code=401, detail="Unauthorized")
    if user.role is Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    all_docs = collection.get()
    all_ids = all_docs.get('ids', [])

    if all_ids:
        # Delete all documents
        collection.delete(ids=all_ids)

    return {"message": "All files deleted successfully."}

@dashboard_router.post("/add_student")
async def add_student(request: Request):

    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email must be provided")

    course_id = request.query_params.get("course_id") or data.get("course_id")
    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID must be provided")

    # Retrieve the student record by email; if it doesn't exist, create it.
    user_record = read_user_by_email(email)
    if user_record is None:
        if not create_user(email, email, 'student'):
            raise HTTPException(status_code=500, detail="Failed to create student")
        user_record = read_user_by_email(email)
        if user_record is None:
            raise HTTPException(status_code=500, detail="Student record not found after creation")

    student_id = user_record.id

    # Use the specified course_id
    course_id = request.query_params.get("course_id") or data.get("course_id")
    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID must be provided")

    # Check if the student is already enrolled in the course.
    enrolled_users = read_users_for_course(course_id)
    if str(student_id) in enrolled_users:
        raise HTTPException(status_code=400, detail="Student is already enrolled in course")


    # Enroll the student in the specified course
    success = create_user_course(course_id, str(student_id))
    if not success:
        if str(student_id) not in enrolled_users:
            raise HTTPException(status_code=500, detail="Failed to enroll student in course")

    return {"success": True, "message": "Student added successfully and enrolled in course."}

@dashboard_router.delete("/remove_student")
async def remove_student(request: Request):

    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email must be provided")

    course_id = request.query_params.get("course_id") or data.get("course_id")
    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID must be provided")

    # Retrieve the student record by email
    user_record = read_user_by_email(email)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")

    student_id = user_record.id

    # Attempt to remove the student from the specified course
    success = delete_user_course(course_id, str(student_id))
    if not success:
        # Double-check whether the student is still enrolled in the course
        enrolled_users = read_users_for_course(course_id)
        if str(student_id) in enrolled_users:
            raise HTTPException(status_code=500, detail="Failed to remove student from course")

    return {"success": True, "message": "Student removed from course."}

@dashboard_router.post("/add_students_bulk")
async def add_students_bulk(request: Request, file: UploadFile = File(...), context: dict = Depends(get_context)):
    """
    Bulk add students from a CSV file to a course.
    """

    course_id = request.query_params.get("course_id")
    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID must be provided.")

    content = await file.read()
    decoded_content = content.decode("utf-8")
    
    # Use csv.reader to process the file.
    reader = csv.reader(io.StringIO(decoded_content))
    results = []

    for row in reader:
        if not row:
            continue
        email = row[0].strip()
        if not email:
            continue

        # Try to get the student record by email; if none exists, create one.
        user_record = read_user_by_email(email)
        if user_record is None:
            if not create_user(email, email, 'student'):
                results.append({"email": email, "status": "failed", "detail": "Failed to create student."})
                continue
            user_record = read_user_by_email(email)
            if user_record is None:
                results.append({"email": email, "status": "failed", "detail": "Student record not found after creation."})
                continue
        
        student_id = user_record.id

        enrolled_users = read_users_for_course(course_id)
        if str(student_id) in enrolled_users:
            # Record that this student is already enrolled, and continue to the next record.
            results.append({"email": email, "status": "already enrolled"})
            continue

        # Enroll the student in the specified course.
        success = create_user_course(course_id, str(student_id))
        if not success:
            enrolled_users = read_users_for_course(course_id)
            if str(student_id) not in enrolled_users:
                results.append({"email": email, "status": "failed", "detail": "Failed to enroll student in course."})
                continue
        
        results.append({"email": email, "status": "success"})

    return {"results": results, "message": "Bulk student enrollment completed."}

@dashboard_router.delete("/remove_all_students")
async def remove_all_students(request: Request, context: dict = Depends(get_context)):

    user: User = context.get("user")
    if user is None or user.role == Role.student:
        raise HTTPException(status_code=401, detail="Unauthorized")

    course_id = request.query_params.get("course_id")
    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID must be provided")

    success = delete_all_user_courses(course_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to remove all students from course")

    return {"success": True, "message": "All students have been removed from the course."}