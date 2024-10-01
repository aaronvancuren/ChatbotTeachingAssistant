from starlette.exceptions import HTTPException

from .main import *

async def validate(uid, text : str):
    if (text == ""):
        return HTTPException(500, "Nothing was asked.")
    if (False): #replace with Validation
        return HTTPException(403, "Forbidden Question")
    return text