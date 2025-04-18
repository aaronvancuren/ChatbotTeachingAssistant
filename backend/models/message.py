from backend.models import BaseModel
from psycopg2.extras import RealDictRow

class Message(BaseModel):
    model: str
    prompt: str
    response: str
    
    def __init__(self, row: RealDictRow):
        super().__init__(
            model=row['model'],
            prompt=row['prompt'],
            response=row['response']
        )