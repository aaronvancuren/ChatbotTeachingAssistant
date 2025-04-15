import uuid
from backend.models import UserBase, CourseBase, Message, Role
from psycopg2.extras import RealDictRow

from backend.models.converstation import User_Conversation

class User(UserBase):
    courses: list[CourseBase] = []
    conversation: list[Message] = []
    activeCourse: CourseBase | None = None

    def __init__(self, row: RealDictRow):
        super().__init__(id=row['id'], display_name=row['display_name'], email=row['email'], role=Role[row['role']])
        
    # Get user courses
    def get_courses(self):        
        from backend.database.postgres import read_courses_for_user, read_courses_for_instructor
        if self.role is Role.student:
            updated_user = read_courses_for_user(str(self.id))
            if updated_user is not None:
                self.courses = updated_user
        elif self.role is Role.instructor:
            updated_instructor = read_courses_for_instructor(str(self.id))
            if updated_instructor is not None:
                self.courses = updated_instructor.courses
    
    # Get user conversations by course
    def get_conversations(self, course_id: uuid) -> list[User_Conversation]:
        course = [course for course in self.courses if course.id == course_id][0]
        self.activeCourse = course
        return course.get_conversations(self)
    
    def get_conversation(self, conversation_id: uuid) -> list[Message]:
        from backend.database.postgres import read_messages_from_conversation
        # Get messages from the messages table using the conversation_id
        self.conversation = read_messages_from_conversation(conversation_id)
        return self.conversation
        # Update the conversation property
        
        # Return the conversation (list[message])
        pass