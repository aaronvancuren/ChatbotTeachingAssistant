from backend.models import CourseBase, UserBase

class Course(CourseBase):
    students: list[UserBase]
    
    # Get a list of students
    def get_students() -> list[UserBase]:
        pass
    
    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass