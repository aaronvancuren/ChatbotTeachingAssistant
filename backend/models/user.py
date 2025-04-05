from __future__ import annotations
import uuid
from backend.models import UserBase, CourseBase, Message, Role
from psycopg2.extras import RealDictRow

class User(UserBase):
    courses: list[CourseBase] = []
    
    def __init__(self, email: str, id: uuid):
        #def __init__(self, row: RealDictRow):
        #super().__init__(id=row['id'], display_name=row['display_name'], email=row['email'], role=Role[row['role']])
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
    def get_courses() -> list[CourseBase]:
        pass
    
    # Get user conversations by course
    def get_conversations(self, course_id: uuid.UUID) -> list[Message]:
        # Get the conversation_id from the user_conversations table by using the course_id and id

        # Update the conversation property
        
        # Return the conversation (list[message])
        pass
    
    def get_conversation(self, conversation_id: uuid) -> list[Message]:
        # Get messages from the messages table using the conversation_id
        
        # Update the conversation property
        
        # Return the conversation (list[message])
        pass