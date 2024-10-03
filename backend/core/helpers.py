from starlette.exceptions import HTTPException

async def validate(uid, text : str):
    if (text == ""):
        raise HTTPException(500, "Nothing was asked.")
    if (False): #replace with Validation
        raise HTTPException(403, "Forbidden Question")
    return text