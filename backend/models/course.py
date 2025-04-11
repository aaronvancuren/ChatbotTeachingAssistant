from backend.models import CourseBase, UserBase
from backend.models.user import User

class Course(CourseBase):
    students: list[UserBase]
    
    def get_students(self):
        from backend.database.postgres import read_students_for_course
        self.students = read_students_for_course(str(self.id))
    
    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass