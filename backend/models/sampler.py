import uuid

from backend.models.converstation import Conversation, Model
from backend.models.classes import ClassSection

def CreateSampleClassSections(num = 1):
    tmpList = []
    for i in range(0, num):
        tmpClass = ClassSection()
        tmpClass.id = uuid.uuid4()                          # Replace with UUID of Class
        tmpClass.name = "Intro to C and Unix"                     # Replace with Name of Class
        tmpClass.professor_id = "Zesheng Chen"        # Replace with Professor of Class
        tmpClass.section = "CS 232-01"                                # Replace with Section of Class
        tmpClass.teaching_assistant_id = "Example Student " + str(i)  # Replace with TA
        tmpClass.splash = "/static/assets/20230504-Crecent-Bridge-Drone-TE-001.jpg"
        tmpClass.prompt = (
            "You are a TA for CS 232, introduction to C and Unix"
            "You are a helpful teaching assistant."
            "You should offer guidance to help students understand the material. "
            "You should not provide students with direct solutions to problems. "
            "You should maintain a polite and supportive tone."
            "If you do not know the answer to a question, tell the student that you do not know and instruct them on where to find more information."
            "Only answer questions relevant to the course material."
            "Only use pseudocode to answer coding questions"
        )
        tmpList.append(tmpClass)
    return tmpList

def CreateSampleConversation(UserID : str):
    tmpList = []
    
    EXAMPLE_CONVERSATION = Conversation(UserID, Model.JOHN)
    EXAMPLE_CONVERSATION.name = "CS 232 Help"                      # Replace with Name of conversation
    EXAMPLE_CONVERSATION.classID = uuid.uuid4()                     # Replace with UUID of conversation
    tmpList.append(EXAMPLE_CONVERSATION)
    return tmpList
