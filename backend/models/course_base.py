import uuid
from backend.models import BaseModel, ConfigDict, Subject

class CourseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    instructor_id: uuid.UUID
    display_name: str
    subject: Subject
    course_number: int
    section_number:int
    title: str
    model: str
    prompt: str
    documents_path: str
    image_path: str