"""Initializing the FastAPI application"""

import os

from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates

from backend.api.errors import HTTPError
from backend.api.routes.web import web_router
from backend.api.routes.openai import openai_router
from backend.api.routes.auth import msal_auth
from backend.api.routes.dashboard import dashboard_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# Set up FastAPI settings
app = FastAPI()

# Add Routes
app.include_router(web_router)
app.include_router(openai_router)
app.include_router(msal_auth.router)
app.include_router(dashboard_router)

# Set up pathing to CSS/JS files for Jinja2 Templates
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGINS")],
    allow_origin_regex="https://*",
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Accept", "Accept-Language", "Content-Language", "Content-Type"],
    allow_credentials=True, # When True allow_origins, allow_methods and allow_headers cannot be set to ['*']
    expose_headers=[],
    max_age=600,
)

# Enable Session Management
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
)

# Enables secure HTTPS connections for production
if os.getenv("environment") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)


@app.exception_handler(HTTPError)
@app.exception_handler(404)
@app.exception_handler(RequestValidationError)
async def http_error_handler(request, exc):
    if (isinstance(exc, RequestValidationError)):
        err = HTTPError(422, "Unprocessable Entity")
    else:
        err = HTTPError(exc.status_code, exc.detail)
    return Jinja2Templates(directory='frontend/templates').TemplateResponse('/error.html', {"request": request, "context": err})
