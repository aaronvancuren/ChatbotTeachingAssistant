import os
import uuid

from datetime import datetime
from enum import Enum

from pydantic import ConfigDict
from psycopg2.extras import RealDictRow

class Model(Enum):
    VICTOR = "gpt-3.5-turbo"
    JOHN = "gpt-4o-mini-2024-07-18"
    HEDY = "gpt-4o-mini"
    HENRIETTA = "gpt-4o"

class User_Conversation:
    model_config = ConfigDict(from_attributes=True)

    conversation_id: uuid
    user_id: uuid
    course_id: uuid
    model: Model
    title: str
    created_at: datetime
    archived: bool
    archived_at: datetime

    def __init__(self, row: RealDictRow):
        self.conversation_id = row['conversation_id']
        self.user_id = row['user_id']
        self.course_id = row['course_id']
        self.model = Model(row['model'])
        self.title = row['title']
        self.created_at = row['created_at']
        self.archived = row['archived']
        self.archived_at = row['archived_at']