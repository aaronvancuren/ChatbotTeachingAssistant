from pydantic import BaseModel, ConfigDict
from psycopg2.extras import RealDictRow
from backend.models.role import Role
from backend.models.subject import Subject
from backend.models.message import Message
from backend.models.user_base import UserBase
from backend.models.course_base import CourseBase
from backend.models.user_converstation import UserConversation
from backend.models.user import User
from backend.models.course import Course