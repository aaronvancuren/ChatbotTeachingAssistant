from backend.models.classes import ClassSection

async def get_user_classes(UserID : str) -> list[ClassSection]:
    """
    Returns a list of classes a given UserID is a part of
    Args:
        UserID: a string representing the unique id of the user to query

    Returns:
        A list of ClassSections that the user is a part of
    """
    tmpList = []
    tmpClass = ClassSection()
    tmpClass.id = "00000-1111-2222-33333"           # Replace with UUID of Class
    tmpClass.name = "Example Class"                 # Replace with Name of Class
    tmpClass.professor_id = "Example Professor"        # Replace with Professor of Class
    tmpClass.section = 1                            # Replace with Section of Class
    tmpClass.teaching_assistant_id = "Example Student" # Replace with TA
    tmpList.append(tmpClass)
    
    return tmpList
    