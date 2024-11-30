from typing import List, Tuple

class Conversation:
    id: str         # Unique HashID
    name: str       # Conversation Name
    classID: str    # Class HashID
    discussion: List[Tuple[str, str]]