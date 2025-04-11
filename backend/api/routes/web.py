"""TODO: update docstring"""
from os import getenv
import uuid
from backend.api.errors import HTTPError
from backend.api.routes import get_context
from backend.models.converstation import Model
from backend.models import User, Role

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse

from backend.database.postgres import create_user_conversation, read_conversations_by_user, read_messages_from_conversation
from backend.models.converstation import Model

web_router = APIRouter()

page_templates = Jinja2Templates(directory='frontend/templates')

#region Endpoint Pages

# Note: Any page will need to follow this format:
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
@web_router.get("/")
async def homepage(request: Request, context: dict = Depends(get_context)):
    """
    Main index page of application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Index Web Page Response
    """  
    if context.get("logged_in"):
        convos = read_conversations_by_user(context['user'].id, getenv("COURSE_ID"))
        if len(convos) == 0:
            convos = [create_user_conversation(getenv("COURSE_ID"), context['user'].id, Model.JOHN.value.lower(), "CS 232 Help")]
        context.update({"conversation_list": convos})
    return page_templates.TemplateResponse('index.html', {"request": request, "context": context})

# The Chat Page
@web_router.get("/chat")
async def chatpage(request: Request, chatID: str, context: dict = Depends(get_context)):
    """
    Chat page of application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Chat Web Page Response if the user has authenticated. Otherwise, it
        will return a 401 error page.
    """
    if not context.get("logged_in"):
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    user: User = context.get("user")

    userConvos = read_conversations_by_user(user.id, getenv("COURSE_ID"))
    try:
        conversation = [userConvo for userConvo in userConvos if str(userConvo.conversation_id) == chatID][0]
        context.update({"conversation_list": userConvos})
        context.update({"conversation_data": read_messages_from_conversation(chatID)})
        context.update({"conversation_model": conversation.model})
        context.update({"chatID": chatID})
        
        return page_templates.TemplateResponse('chat.html', {"request": request, "context": context})
    except Exception as e:
        raise HTTPError(status_code=404, detail="Chat not found")

@web_router.post("/addChat")
async def addChat(request: Request, context: dict = Depends(get_context)):
    role: Role = context.get("user").role
    if role is not Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    reqBody = await request.json()
    newConvo = create_user_conversation(getenv("COURSE_ID"), context['user'].id, reqBody['model'], "CS 232 Help")
    return PlainTextResponse(f"/chat?chatID={str(newConvo)}")

@web_router.get("/profile")
async def profilepage(request: Request, context: dict = Depends(get_context)):
    """
    Profile page of application
    Args:
        request: the data contained in the request that the server received
    """
    if not context.get("logged_in"):
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    return page_templates.TemplateResponse('profile.html', {"request": request, "context": context})

#endregion

#region Error Pages

async def Error_401(request: Request, context: dict):
    """
    401 page of application
    Args:
        request: the data contained in the request that the server received
        user_context: the authentication context attached to the request
    
    Returns:

        401 error page
    """
    return page_templates.TemplateResponse('/errors/401.html', {"request": request, "context": context})

#endregion
