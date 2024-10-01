from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')

# Note: Any page will need to follow this format: 
# async def <description>page(request):
#       return templates.TemplateResponse(request, <PATH>)

# The homepage
async def homepage(request):
    return templates.TemplateResponse(request, 'index.html')

# The Chat Page
async def chatpage(request):
    return templates.TemplateResponse(request, 'chat.html')