from starlette.responses import RedirectResponse

from ... core import page_templates, error_templates

from .. authentication.Microsoft.auth_config import *

#region Endpoint Pages

# Note: Any page will need to follow this format: 
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage

async def homepage(request):
    return page_templates.TemplateResponse(request, 'index.html', loggedin=ACCOUNT_LOGGED_IN)

# The Chat Page
async def chatpage(request):
    return page_templates.TemplateResponse(request, 'chat.html', loggedin=ACCOUNT_LOGGED_IN)

#endregion

#region Error Pages

#endregion