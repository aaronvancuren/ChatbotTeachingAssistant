import logging

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory='templates')

#region HTML Pages
# Note: Any page will need to follow this format: 
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
async def homepage(request):
    print(request)
    return templates.TemplateResponse(request, 'index.html')

# The Chat Page
async def chatpage(request):
    print(request)
    return templates.TemplateResponse(request, 'chat.html')

#endregion

# This code is our web page map.
# Root directory is '/', this is defaulted to the 'index.html' page.
# Mount('/static', ...) needs to be present to mount the directory where the pages are.
# When a new page is added, insert it above Mount('/static', ...) and give it
# a descriptive file path.
routes = [
    Route('/', endpoint=homepage),
    Route('/chat', endpoint=chatpage),
    Mount('/static', StaticFiles(directory='templates'), name='static')
]

app = Starlette(debug=True,routes=routes)