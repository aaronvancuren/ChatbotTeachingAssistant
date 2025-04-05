import uuid
from backend.models import UserBase, CourseBase, Message, Role
from psycopg2.extras import RealDictRow

class User(UserBase):
    courses: list[CourseBase] = []
    
    def __init__(self, row: RealDictRow):
        super().__init__(id=row['id'], display_name=row['display_name'], email=row['email'], role=Role[row['role']])
        
    # Get user courses
    def get_courses() -> list[CourseBase]:
        pass
    
    # Get user conversations by course
    def get_conversations(self, course_id: uuid) -> list[Message]:
        # Get the conversation_id from the user_conversations table by using the course_id and id

        # Update the conversation property
        
        # Return the conversation (list[message])
        pass
    
    def get_conversation(self, conversation_id: uuid) -> list[Message]:
        # Get messages from the messages table using the conversation_id
        
        # Update the conversation property
        
        # Return the conversation (list[message])
        pass