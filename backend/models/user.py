import uuid
from backend.database.postgres import *

from backend.models.role import Role
from backend.models.message import Message
from backend.models.course import Course

class User:
    id: uuid
    display_name: str
    email: str
    role: Role
    courses: list[Course] = []
    conversation: list[Message] = []
    
    def __init__(self, email: str, id: uuid):
        # Find the user in the database
        user: RealDictRow = read_user_by_email(email)
        if(user is None):
            # you have not been invited
            pass
        
        # If found, inspect user id
        self.id:uuid = uuid.UUID(user["id"])
        if(self.id is None):
            set_user_id(id, email)
            pass
        
        # If id is null, update user with id argument (first time logging into application)
        
        # If id is not null compare to the argument id, throw an invalid user error if they do not match
        pass
    
    # Get user courses
    def get_courses() -> list[Course]:
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
    