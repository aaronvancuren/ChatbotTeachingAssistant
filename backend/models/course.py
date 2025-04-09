import uuid
from backend.models import CourseBase, UserBase
from backend.database.postgres import read_users_for_course, read_user_by_id
from backend.models.user import User

class Course(CourseBase):
    students: list[UserBase]
    
    # def __init__(self):
    #     pass
    
    def get_students(self) -> list[UserBase]:
        # Get all user IDs (as strings) for this course
        user_ids = read_users_for_course(str(self.id))

        students = []
        # For each user ID, load user details from the database
        for uid in user_ids:
            user_row = read_user_by_id(uid)
            if user_row is not None:
                students.append(User(user_row))
        return students
    
    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass