import uuid

from backend.models.converstation import Conversation
from backend.models.classes import ClassSection

def CreateSampleClassSections(num = 1):
    tmpList = []
    for i in range(0, num):
        tmpClass = ClassSection()
        tmpClass.id = uuid.uuid4()                          # Replace with UUID of Class
        tmpClass.name = "Example Class " + str(i + 1)                     # Replace with Name of Class
        tmpClass.professor_id = "Example Professor" + str(i)         # Replace with Professor of Class
        tmpClass.section = str(i)                                # Replace with Section of Class
        tmpClass.teaching_assistant_id = "Example Student " + str(i)  # Replace with TA
        tmpClass.splash = "https://plus.unsplash.com/premium_photo-1661872817492-fd0c30404d74?fm=jpg&q=60&w=300&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29tcHV0ZXIlMjBzY2llbmNlfGVufDB8fDB8fHww"
        tmpList.append(tmpClass)
    return tmpList

def CreateSampleConversation():
    tmpList = []
    
    EXAMPLE_CONVERSATION = Conversation()
    EXAMPLE_CONVERSATION.id = uuid.uuid4()
    EXAMPLE_CONVERSATION.name = "Introduction"                      # Replace with Name of conversation
    EXAMPLE_CONVERSATION.classID = uuid.uuid4()                     # Replace with UUID of Class
    EXAMPLE_CONVERSATION.discussion = []
    EXAMPLE_CONVERSATION.discussion.append({'role': 'user', 'content': 'Hello! Can you introduce yourself?'})
    EXAMPLE_CONVERSATION.discussion.append({'role': 'assistant', 'content': 'My name is Victor. I am an AI created by OpenAI.'})

    tmpList.append(EXAMPLE_CONVERSATION)
    return tmpList
