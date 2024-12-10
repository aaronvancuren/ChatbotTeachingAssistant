import uuid

from backend.models.classes import ClassSection
from backend.models.sampler import CreateSampleClassSections

def get_user_classes(UserID : str) -> list[ClassSection]:
    """
    Returns a list of classes a given UserID is a part of
    Args:
        UserID: a string representing the unique id of the user to query

    Returns:
        A list of ClassSections that the user is a part of
    """
    # SEARCH DB
    return CreateSampleClassSections()
    