"""TODO: update docstring"""
from os import getenv
import uuid
from backend.api.errors import HTTPError
from backend.api.routes import get_context
from backend.models.converstation import Model
from backend.models import User, Role

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse, RedirectResponse

from backend.database.postgres import create_user_conversation, read_conversations_by_user, read_messages_from_conversation

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
    return page_templates.TemplateResponse('index.html', {"request": request, "context": context})

# The Chat Page
@web_router.get("/chat/{courseID}")
async def populate_chats(request: Request, courseID: str, context: dict = Depends(get_context)):
    if not context.get("logged_in"):
        raise HTTPError(status_code=401, detail="Unauthorized")
    user: User = context.get("user")
    convo = user.get_conversations(uuid.UUID(courseID))
    context.update({"user": user})
    return RedirectResponse(f"/chat/{courseID}/{convo[0].conversation_id}")

@web_router.get("/chat/{courseID}/{chatID}")
async def chatpage(request: Request, courseID: str, chatID: str, context: dict = Depends(get_context)):
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
    user.get_conversations(uuid.UUID(courseID))
    user.get_conversation(uuid.UUID(chatID))
    context.update({"user": user})
    return page_templates.TemplateResponse('chat.html', {"request": request, "context": context})
    

@web_router.post("/addChat/{classID}")
async def addChat(request: Request, classID: str, context: dict = Depends(get_context)):
    role: Role = context.get("user").role
    if role is not Role.student:
        raise HTTPError(status_code=401, detail="Unauthorized")
    
    reqBody = await request.json()
    print(classID)
    newConvo = create_user_conversation(classID, context['user'].id, reqBody['model'], "New Conversation")
    return PlainTextResponse(f"/chat/{classID}/{newConvo}")

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