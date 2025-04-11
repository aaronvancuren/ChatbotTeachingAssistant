import uuid
from backend.models import BaseModel, ConfigDict, Message, Role

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    display_name: str
    email: str
    role: Role
    conversation: list[Message] = []