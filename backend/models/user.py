import uuid
from backend.models import UserBase, CourseBase, Message, Role, UserConversation
from psycopg2.extras import RealDictRow

class User(UserBase):
    courses: list[CourseBase] = []
    conversation: list[Message] = []
    activeCourse: CourseBase | None = None
    activeConversation: object | None = None

    # Get user courses
    def get_courses(self):        
        from backend.database.postgres import read_courses_for_user, read_courses_for_instructor
        if self.role is Role.student:
            self.courses = read_courses_for_user(str(self.id))
        elif self.role is Role.instructor:
            self.courses = read_courses_for_instructor(str(self.id))
    
    # Get user conversations by course
    def get_conversations(self, course_id: uuid) -> list[UserConversation]:
        from backend.models.course import Course
        self.activeCourse: Course = [course for course in self.courses if course.id == course_id][0]
        return self.activeCourse.get_conversations(self)
    
    def find_conversation(self, conversation_id: uuid) -> UserConversation:
        if self.courses == []:
            self.get_courses()
        for course in self.courses:
            for conversation in self.get_conversations(course.id):
                if conversation.conversation_id == conversation_id:
                    return conversation
        raise Exception("Conversation not found")

    def get_conversation(self, conversation_id: uuid) -> tuple[UserConversation, Message]:
        from backend.database.postgres import read_messages_from_conversation
        self.conversation = read_messages_from_conversation(conversation_id)
        self.activeConversation = self.find_conversation(conversation_id)
        return { 'conversation': self.activeConversation, 'messages': self.conversation }
    
    def __init__(self, row: RealDictRow):
        super().__init__(
            id=row['id'],
            display_name=row['display_name'],
            email=row['email'],
            role=Role[row['role']]
        )