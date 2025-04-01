from __future__ import annotations
import uuid
from backend.database.postgres import *

from backend.models.role import Role
from backend.models.message import Message

class User:
    id: uuid.UUID
    display_name: str
    email: str
    role: Role
    courses: list["Course"] = []
    conversation: list[Message] = []
    
    def __init__(self, email: str, id: uuid.UUID):
        # Look up the user by email
        user_record = read_user_by_email(email)
        print("DEBUG: Initial user_record =", user_record)
        if user_record is None:
            # No invitation exists; create a new student record.
            from backend.database.postgres import create_user, set_user_id
            if not create_user(email, email, 'student'):
                raise ValueError("Failed to create user")
            # Re-read the user record after creation
            user_record = read_user_by_email(email)
            print("DEBUG: User record after creation =", user_record)
            if user_record is None:
                raise ValueError("User still not found after creation")
        
        # Initialize fields from the DB
        self.email = user_record["email"]
        self.display_name = user_record["display_name"]

        role_from_db = user_record["role"]
        print("DEBUG: Role from DB =", role_from_db)
        if isinstance(role_from_db, str):
            role_from_db = role_from_db.lower()
            if role_from_db == "student":
                self.role = Role.STUDENT
            elif role_from_db == "instructor":
                self.role = Role.INSTRUCTOR
            elif role_from_db == "admin":
                self.role = Role.ADMIN
            else:
                raise ValueError(f"Invalid role stored in DB: {role_from_db}")
        else:
            self.role = Role(role_from_db)
        
        # Set UUID
        from backend.database.postgres import set_user_id
        print("DEBUG: Setting user id with", str(id))
        if not set_user_id(str(id), email):
            print("WARNING: set_user_id returned False")
        self.id = id
    
    # Get user courses
    def get_courses(self) -> list[Course]:
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