"""TODO: update docstring"""
from backend.api.routes.auth import get_context
from backend.database.database_class_sections import get_user_classes
from backend.database.database_user_conversations import get_user_conversations, add_user_conversation
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_msal.models import IDTokenClaims, TokenStatus
from fastapi.responses import PlainTextResponse

web_router = APIRouter()

page_templates = Jinja2Templates(directory='frontend/templates')

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
            context.update({"class_list": get_user_classes(claims.user_id)})
            context.update({"conversation_list": get_user_conversations(claims.user_id)})

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
            context.update({"display_name": claims.display_name})
            context.update({"conversation_list": get_user_conversations(claims.user_id)})
            context.update({"conversation_data": next(
                (convo for convo in get_user_conversations(claims.user_id) 
                 if str(convo.id) == chatID), None).getDiscussion()})
            context.update({"chatID": chatID})

            return page_templates.TemplateResponse('chat.html', {"request": request, "context": context})

    return await Error_401(request, context)

@web_router.get("/addChat")
async def addChat(request: Request, context: dict = Depends(get_context)):
    if context.get("id_token") is not None:
        claims: IDTokenClaims = IDTokenClaims.decode_id_token(context.get("id_token"))
        if(claims is not None and claims.validate_token() == TokenStatus.VALID):
            newConvo = add_user_conversation(claims.user_id)
            return PlainTextResponse(str(newConvo.id))

    return await Error_401(request, context)

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