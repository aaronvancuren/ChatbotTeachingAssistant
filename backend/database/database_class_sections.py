import uuid

from backend.models.classes import ClassSection

def get_user_classes(UserID : str) -> list[ClassSection]:
    """
    Returns a list of classes a given UserID is a part of
    Args:
        UserID: a string representing the unique id of the user to query

    Returns:
        A list of ClassSections that the user is a part of
    """
    tmpList = []
    tmpClass = ClassSection()
    tmpClass.id = uuid.uuid4()                          # Replace with UUID of Class
    tmpClass.name = "Example Class"                     # Replace with Name of Class
    tmpClass.professor_id = "Example Professor"         # Replace with Professor of Class
    tmpClass.section = 1                                # Replace with Section of Class
    tmpClass.teaching_assistant_id = "Example Student"  # Replace with TA
    tmpClass.splash = "https://plus.unsplash.com/premium_photo-1661872817492-fd0c30404d74?fm=jpg&q=60&w=300&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29tcHV0ZXIlMjBzY2llbmNlfGVufDB8fDB8fHww"
    tmpList.append(tmpClass)
    
    return tmpList
    