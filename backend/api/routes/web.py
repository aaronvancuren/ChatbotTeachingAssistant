from ... core import page_templates, error_templates

from .. authentication.Microsoft import *

#region Endpoint Pages

# Note: Any page will need to follow this format: 
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage

async def homepage(request):
    userContext = await get_user_context(request)
    return page_templates.TemplateResponse(request, 'index.html', context=userContext)

# The Chat Page
async def chatpage(request):
    userContext = await get_user_context(request)
    if userContext["user_id"] == None:
        return await Error_401(request, userContext)
    else:
        return page_templates.TemplateResponse(request, 'chat.html', context=userContext)

#endregion

#region Error Pages

async def Error_401(request, user_context):
    return error_templates.TemplateResponse(request, '/errors/401.html', context=user_context)

#endregion