import uuid
from backend.models import CourseBase, UserBase

class Course(CourseBase):
    students: list[UserBase]
    
    def __init__(self):
        pass
    
    # Get a list of students
    def get_students() -> list[UserBase]:
        pass
    
    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass

    @classmethod
    def add_student(cls, course_id: str, student: User) -> bool:
        from backend.database.postgres import create_user_course
        # Call the function to insert a row into user_courses
        return create_user_course(course_id, str(student.id))