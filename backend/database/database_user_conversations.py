import uuid

from backend.database.database_class_sections import get_user_classes
from backend.models.converstation import Conversation, Model
from backend.models.sampler import CreateSampleConversation

DEMO_LIST = []

def get_user_conversations(UserID : str) -> list[Conversation]:
    """
    Returns a list of conversations a given UserID is a part of
    Args:
        UserID: a string representing the unique id of the user to query

    Returns:
        A list of conversations that the user is a part of
    """
    li = [convo for convo in DEMO_LIST if convo.user_id == UserID]
    if (len(li) == 0):
        add_user_conversation(UserID, Model.JOHN)
        li = [convo for convo in DEMO_LIST if convo.user_id == UserID]
    return li                                # Replace with DATABASE CALLS
    

#TODO need to reevaluate this method and the use of the get_user_classes method
def add_user_conversation(UserID : str, model: Model):
    tmpConvo = Conversation(UserID, assistant=model,class_prompt=get_user_classes(UserID)[0].prompt)
    tmpConvo.id = uuid.uuid4()
    tmpConvo.name = f"New chat with {model.name.title()}"                      # Replace with Name of conversation
    tmpConvo.classID = uuid.uuid4()                 # Replace with UUID of conversation
    DEMO_LIST.append(tmpConvo)                      # Replace with DATABASE CALLS
    return tmpConvo