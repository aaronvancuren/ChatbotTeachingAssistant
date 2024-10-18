"""TODO: update docstring"""
from backend.api.authentication.Microsoft import get_user_context
from backend.core import page_templates
from fastapi import APIRouter

web_router = APIRouter()
#region Endpoint Pages

# Note: Any page will need to follow this format:
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
@web_router.get("/")
async def homepage(request):
    """TODO: update docstring"""
    userContext = await get_user_context(request)
    return page_templates.TemplateResponse(request, 'index.html', context=userContext)

# The Chat Page
@web_router.get("/chat")
async def chatpage(request):
    """TODO: update docstring"""
    userContext = await get_user_context(request)
    if userContext["user_id"] == None:
        return await Error_401(request, userContext)
    else:
        return page_templates.TemplateResponse(request, 'chat.html', context=userContext)
#endregion

#region Error Pages

async def Error_401(request, user_context):
    return page_templates.TemplateResponse(request, '/errors/401.html', context=user_context)

#endregion
