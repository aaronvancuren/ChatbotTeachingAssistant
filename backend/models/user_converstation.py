import uuid
from backend.models import BaseModel, ConfigDict, RealDictRow

class UserConversation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    conversation_id: uuid.UUID | None = uuid.uuid4()
    user_id: uuid.UUID | None = uuid.uuid4()
    course_id: uuid.UUID | None = uuid.uuid4()
    model: str | None = "gpt-4o-mini-2024-07-18"
    title: str | None = "New Conversation"

    def getModelAlias(self):
        if(self.model == "gpt-3.5-turbo"):
            return "VICTOR"
        elif (self.model == "gpt-4o-mini-2024-07-18"):
            return "JOHN"
        elif (self.model == "gpt-4o-mini"):
            return "HEDY"
        elif (self.model == "gpt-4o"):
            return "HENRIETTA"

    def __init__(self, row: RealDictRow):
        super().__init__(
        conversation_id=row['conversation_id'],
        user_id=row['user_id'],
        course_id=row['course_id'],
        model=row['model'],
        title=row['title'])