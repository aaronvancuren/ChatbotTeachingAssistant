"""TODO: update docstring"""
from os import getenv
import uuid
from backend.api.errors import HTTPError
from backend.api.routes.auth import get_context
from backend.database.database_class_sections import get_user_classes
from backend.database.database_user_conversations import get_user_conversations, add_user_conversation
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_msal.models import IDTokenClaims, TokenStatus
from fastapi.responses import PlainTextResponse

from backend.database.postgres import create_user_conversation, get_conversation_data, read_conversations_by_user, read_messages_from_conversation
from backend.models.converstation import Conversation, Model

web_router = APIRouter()

page_templates = Jinja2Templates(directory='frontend/templates')
page_templates.env.filters['GetConvoData'] = get_conversation_data

#region Endpoint Pages

# Note: Any page will need to follow this format:
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
@web_router.get("/")
async def homepage(request : Request, context: dict = Depends(get_context)):
    """
    Main index page of application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Index Web Page Response
    """
    if context.get("id_token") is not None:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(context.get("id_token"))
        if claims is not None and claims.validate_token() == TokenStatus.VALID:
            context.update({"display_name": claims.display_name})
            context.update({"class_list": get_user_classes(claims.user_id)}) #TODO update method of getting student classes
            convos = read_conversations_by_user(claims.user_id, getenv("COURSE_ID"))
            if len(convos) == 0:
                convos = [create_user_conversation(getenv("COURSE_ID"), claims.user_id, "CS 232 Help")]
    
            context.update({"conversation_list": convos}) #TODO update method of getting conversations for classes. Need to discuss when we should be getting the conversations

    return page_templates.TemplateResponse('index.html', {"request": request, "context": context})

# The Chat Page
@web_router.get("/chat")
async def chatpage(request : Request, chatID : str, context: dict = Depends(get_context)):
    """
    Chat page of application
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Chat Web Page Response if the user has authenticated. Otherwise, it
        will return a 401 error page.
    """
    if context.get("id_token") is not None:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(context.get("id_token"))
        if(claims is not None and claims.validate_token() == TokenStatus.VALID):
            userConvos = read_conversations_by_user(claims.user_id, getenv("COURSE_ID"))
            try:
                conversation = read_messages_from_conversation(chatID)
                    
                context.update({"display_name": claims.display_name})
                context.update({"conversation_list": userConvos})
                context.update({"conversation_data": conversation}) #TODO update method of getting the discussion (should be conversation) Need Neal to clarify method purpose.
                context.update({"conversation_model": Model.JOHN})
                context.update({"chatID": chatID})

                return page_templates.TemplateResponse('chat.html', {"request": request, "context": context})
            except Exception as e:
                raise HTTPError(status_code=404, detail="Chat not found")

    raise HTTPError(status_code=401, detail="Unauthorized")

@web_router.post("/addChat")
async def addChat(request: Request, context: dict = Depends(get_context)):
    reqBody = await request.json()
    if context.get("id_token") is not None:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(context.get("id_token"))
        if(claims is not None and claims.validate_token() == TokenStatus.VALID):
            newConvo = create_user_conversation(getenv("COURSE_ID"), claims.user_id, "CS 232 Help")
            return PlainTextResponse(f"/chat?chatID={str(newConvo)}")

    raise HTTPError(status_code=401, detail="Unauthorized")

@web_router.get("/profile")
async def profilepage(request : Request, context: dict = Depends(get_context)):
    """
    Profile page of application
    Args:
        request: the data contained in the request that the server received
    """
    if context.get("id_token") is not None:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(context.get("id_token"))
        if(claims is not None and claims.validate_token() == TokenStatus.VALID):
            context.update({"display_name": claims.display_name})
            context.update({"id": claims.user_id})
            context.update({"user_email": claims.preferred_username})
            return page_templates.TemplateResponse('profile.html', {"request": request, "context": context})
    raise HTTPError(status_code=401, detail="Unauthorized")

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