from pydantic import BaseModel

class Message(BaseModel):
    """OpenAI message model"""
    content: str