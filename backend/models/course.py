from backend.models import CourseBase, UserBase, Subject, UserConversation, RealDictRow

class Course(CourseBase):
    students: list[UserBase] | None = []
    conversations: list[UserConversation] | None = []

    def get_students(self):
        from backend.database.postgres import read_students_for_course
        self.students = read_students_for_course(str(self.id))
    
    def get_conversations(self, user: UserBase) -> list[UserConversation]:
        from backend.database.postgres import read_conversations_by_user
        self.conversations = read_conversations_by_user(user.id, self.id)
        return self.conversations
    
    def __init__(self, row: RealDictRow):
        super().__init__(
        id=row['id'],
        instructor_id=row['instructor_id'],
        display_name=row['display_name'],
        subject=Subject[row['subject']],
        course_number=row['course_number'],
        section_number=row['section_number'],
        title=row['title'],
        model=row['model'],
        prompt=row['prompt'],
        documents_path=row['documents_path'],
        image_path=row['image_path']
    )
