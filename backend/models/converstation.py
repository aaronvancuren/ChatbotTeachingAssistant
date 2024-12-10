from typing import List, Tuple
import uuid

class Conversation:
    id: str         # Unique HashID
    name: str       # Conversation Name
    classID: str    # Class HashID
    discussion: List[Tuple[str, str]]

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.discussion = []