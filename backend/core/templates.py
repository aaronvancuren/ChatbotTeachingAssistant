from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.templating import Jinja2Templates

page_templates = Jinja2Templates(directory='frontend/templates')
error_templates = Jinja2Templates(directory='frontend/templates/errors')