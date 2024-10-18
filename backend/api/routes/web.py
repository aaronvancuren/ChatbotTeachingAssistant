"""TODO: update docstring"""
from backend.api.authentication.Microsoft import get_user_context
from backend.core.templates import page_templates
from fastapi import APIRouter, Request

web_router = APIRouter()
#region Endpoint Pages

# Note: Any page will need to follow this format:
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
@web_router.get("/")
async def homepage(request : Request):
    """
    Main index page of application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Index Web Page Response
    """
    userContext = await get_user_context(request) # User Authentication information
    return page_templates.TemplateResponse('index.html', {"request": request, **userContext})

# The Chat Page
@web_router.get("/chat")
async def chatpage(request : Request):
    """
    Chat page of application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Chat Web Page Response if the user has authenticated. Otherwise, it
        will return a 401 error page.
    """
    userContext = await get_user_context(request)
    if userContext["user_id"] == None:
        return await Error_401(request, userContext)
    else:
        return page_templates.TemplateResponse('chat.html', {"request": request, **userContext})
#endregion

#region Error Pages

async def Error_401(request: Request, user_context):
    """
    401 page of application
    Args:
        request: the data contained in the request that the server received
        user_context: the authentication context attached to the request
    
    Returns:
        401 error page
    """
    return page_templates.TemplateResponse('/errors/401.html', {"request": request, **user_context})

#endregion