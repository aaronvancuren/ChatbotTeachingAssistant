from backend.models import BaseModel

class Message(BaseModel):
    model: str
    prompt: str
    response: str
    
    def __init__(self):
        pass