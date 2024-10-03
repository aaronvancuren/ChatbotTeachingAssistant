from ...core import page_templates, error_templates
#region Endpoint Pages

# Note: Any page will need to follow this format: 
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
async def homepage(request):
    return page_templates.TemplateResponse(request, 'index.html')

# The Chat Page
async def chatpage(request):
    return page_templates.TemplateResponse(request, 'chat.html')

#endregion

#region Error Pages

# 404 Page
async def not_found(request, exc):
    return error_templates.TemplateResponse(request, '404.html')

#endregion