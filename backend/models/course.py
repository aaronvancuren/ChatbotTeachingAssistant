from backend.models import CourseBase, UserBase
from backend.models.converstation import User_Conversation

class Course(CourseBase):
    students: list[UserBase] | None = []

    def get_students(self):
        from backend.database.postgres import read_students_for_course
        self.students = read_students_for_course(str(self.id))
    
    def get_conversations(self, user: UserBase) -> list[User_Conversation]:
        from backend.database.postgres import read_conversations_by_user
        self.conversations = read_conversations_by_user(user.id, self.id)
        return self.conversations

    # Get a list of documents
    def get_documents(): # What is the type?
        # Retrieve the list of documents from the chroma database using documents_path
        pass