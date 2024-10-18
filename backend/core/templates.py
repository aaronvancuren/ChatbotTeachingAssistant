"""Sets up templating directories"""

from fastapi.templating import Jinja2Templates

page_templates = Jinja2Templates(directory='frontend/templates')
error_templates = Jinja2Templates(directory='frontend/templates/errors')
