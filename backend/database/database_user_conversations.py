import uuid

from backend.models.converstation import Conversation
from backend.models.sampler import CreateSampleConversation

DEMO_LIST = CreateSampleConversation()

def get_user_conversations(UserID : str) -> list[Conversation]:
    """
    Returns a list of conversations a given UserID is a part of
    Args:
        UserID: a string representing the unique id of the user to query

    Returns:
        A list of conversations that the user is a part of
    """
    return DEMO_LIST                                # Replace with DATABASE CALLS
    

def add_user_conversation(UserID : str):

    tmpConvo = Conversation()
    tmpConvo.id = uuid.uuid4()
    tmpConvo.name = "New Chat"                      # Replace with Name of conversation
    tmpConvo.classID = uuid.uuid4()                     # Replace with UUID of Class
    DEMO_LIST.append(tmpConvo)                      # Replace with DATABASE CALLS
    return tmpConvo