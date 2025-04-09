import uuid
from backend.models import UserBase, CourseBase, Message, Role
from psycopg2.extras import RealDictRow
from backend.models.subject import Subject

class User(UserBase):
    courses: list[CourseBase] = []
    
    def __init__(self, row: RealDictRow):
        super().__init__(id=row['id'], display_name=row['display_name'], email=row['email'], role=Role[row['role']])
        
    # Get user courses
    def get_courses(self):
        from backend.database.postgres import read_courses_for_user
        from backend.models.course import Course
        # Query the DB to retrieve classes for this user
        class_list = read_courses_for_user(str(self.id))

        # Convert each row/dict into a Course
        courses = []
        for class_info in class_list:
            raw_subject = class_info["subject"]
            subject_val = Subject[raw_subject.upper()]

            c = Course(
                id=class_info["id"],
                instructor_id=class_info["instructor_id"],
                display_name=class_info["display_name"],
                subject=subject_val,
                course_number=class_info["course_number"],
                section_number=class_info["section_number"],
                title=class_info["title"],
                model=class_info["model"],
                prompt=class_info["prompt"],
                documents_path=class_info["documents_path"],
                image_path=class_info["image_path"],
                students=[]
            )

            c.students = c.get_students()

            courses.append(c)
        self.courses = courses
    
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