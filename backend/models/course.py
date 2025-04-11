from backend.models import CourseBase, UserBase
from backend.models.user import User

class Course(CourseBase):
    students: list[UserBase]
    
    def get_students(self):
        from backend.database.postgres import read_students_for_course
        # Get all user rows (as RealDictRow objects) for this course
        user_rows = read_students_for_course(str(self.id))

        students = []
        # For each user row, instantiate a User
        for user_row in user_rows:
            if user_row is not None:
                students.append(User(user_row))
        self.students = students
    
    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass