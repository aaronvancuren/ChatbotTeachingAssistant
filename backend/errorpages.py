from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend/errors')

async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request, '404.html')
