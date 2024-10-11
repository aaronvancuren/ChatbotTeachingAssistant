"""TODO: update docstring"""
from backend.core import page_templates
#region Endpoint Pages

# Note: Any page will need to follow this format:
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
@app.get("/")
async def homepage(request):
    """TODO: update docstring"""
    return page_templates.TemplateResponse(request, 'index.html')

# The Chat Page
@app.get("/chat")
async def chatpage(request):
    """TODO: update docstring"""
    return page_templates.TemplateResponse(request, 'chat.html')

#endregion

#region Error Pages

#endregion
