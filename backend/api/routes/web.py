"""TODO: update docstring"""
from backend.api.authentication.Microsoft import get_user_context
from backend.core.templates import page_templates, error_templates
from fastapi import APIRouter, Request

web_router = APIRouter()
#region Endpoint Pages

# Note: Any page will need to follow this format:
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
@web_router.get("/")
async def homepage(request : Request):
    """TODO: update docstring"""
    userContext = await get_user_context(request)
    return page_templates.TemplateResponse('index.html', {"request": request, **userContext})

# The Chat Page
@web_router.get("/chat")
async def chatpage(request : Request):
    """TODO: update docstring"""
    userContext = await get_user_context(request)
    if userContext["user_id"] == None:
        return await Error_401(request, userContext)
    else:
        return page_templates.TemplateResponse('chat.html', {"request": request, **userContext})
#endregion

#region Error Pages

async def Error_401(request: Request, user_context):
    return error_templates.TemplateResponse('/errors/401.html', {"request": request, **user_context})

#endregion
