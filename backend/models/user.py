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
        """
        Fetches all courses that this user is enrolled in (or teaches).
        Calls get_user_classes(user_id) from your database_class_sections, then
        turns each record into a Course object.
        """
        from backend.models.course import Course
        from backend.database.database_class_sections import get_user_classes
        
        db_course_dicts = get_user_classes(str(self.id))
        self.courses = [Course(**course_dict) for course_dict in db_course_dicts]
        return self.courses
    
    # Get user conversations by course
    def get_conversations(self, course_id: uuid.UUID) -> list[Message]:
        """
        Fetch all messages across *all* conversation threads for a given course ID.
        In practice, you might want to fetch entire conversation objects
        or handle them differently, but here we gather all messages
        for demonstration purposes.
        """
        from backend.models.converstation import Conversation, Model

        conv_records = read_conversations_by_user(str(self.id), str(course_id))
        conversation_objs = []

        for record in conv_records:
            # Create a new Conversation object
            assistant_model = record.get("model")
            # Fallback if DB lacks or uses an unknown model
            if assistant_model not in [m.value for m in Model]:
                assistant_model = Model.JOHN.value

            conv = Conversation(
                user_id=str(self.id),
                assistant=Model(assistant_model),
                class_prompt=record.get("class_prompt")
            )

            # Overwrite these fields if present
            conv.id = str(record.get("id"))
            conv.name = record.get("name", "")
            conv.classID = record.get("class_id", "")

            # Now load all messages for that conversation
            raw_msgs = read_messages_from_conversation(str(record.get("id")))
            for m in raw_msgs:
                # Add each message to the conversation's discussion
                role = m.get("role")
                content = m.get("content")
                # If your DB uses "prompt" & "response" columns, adapt as needed
                if not role and "prompt" in m:
                    role = "user"
                    content = m["prompt"]
                elif not role and "response" in m:
                    role = "assistant"
                    content = m["response"]

                conv.discussion.append({
                    "role": role,
                    "content": content
                })

            conversation_objs.append(conv)

        self.conversation = conversation_objs
        return conversation_objs
    
    # def get_conversation(self, conversation_id: uuid.UUID) -> list[Message]:
    #     """
    #     Fetches all messages for a single conversation identified by conversation_id.
    #     """
    #     from backend.models.converstation import Conversation, Model

    #     # Assume we have a function to read a single conversation record, or adapt:
    #     record = read_single_conversation(str(conversation_id))  # if needed, else define your own method
    #     if not record:
    #         # If there's no record for that conversation, handle accordingly
    #         raise ValueError("No conversation found for the given ID")

    #     assistant_model = record.get("model")
    #     if assistant_model not in [m.value for m in Model]:
    #         assistant_model = Model.JOHN.value

    #     conv = Conversation(
    #         user_id=str(self.id),
    #         assistant=Model(assistant_model),
    #         class_prompt=record.get("class_prompt")
    #     )

    #     conv.id = str(record.get("id"))
    #     conv.name = record.get("name", "")
    #     conv.classID = record.get("class_id", "")

    #     raw_msgs = read_messages_from_conversation(str(conversation_id))
    #     for m in raw_msgs:
    #         role = m.get("role")
    #         content = m.get("content")
    #         # If your DB uses "prompt" & "response", adapt as needed
    #         if not role and "prompt" in m:
    #             role = "user"
    #             content = m["prompt"]
    #         elif not role and "response" in m:
    #             role = "assistant"
    #             content = m["response"]

    #         conv.discussion.append({
    #             "role": role,
    #             "content": content
    #         })

    #     self.conversation = [conv]
    #     return [conv]