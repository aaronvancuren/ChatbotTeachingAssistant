"""Contains all models required for OpenAI API request/respones"""

from pydantic import BaseModel

class Message(BaseModel):
    """OpenAI request chat message"""
    content: str
