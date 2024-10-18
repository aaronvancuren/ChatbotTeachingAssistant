"""TODO: update docstring"""
from backend.core.templates import page_templates
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
    return page_templates.TemplateResponse(request, 'index.html')

# The Chat Page
@web_router.get("/chat")
async def chatpage(request):
    """TODO: update docstring"""
    return page_templates.TemplateResponse(request, 'chat.html')

#endregion

#region Error Pages

#endregion
