import uuid
from backend.models.user import User
from backend.models.subject import Subject

class Course:
    id: uuid
    instructor_id: uuid
    display_name: str
    subject: Subject
    course_number: int
    section_number:int
    title: str
    model: str
    prompt: str
    documents_path: str
    image_path: str
    students: list[User]
    
    def __init__(self):
        pass
    
    # Get a list of students
    def get_students() -> list[User]:
        pass
    
    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass