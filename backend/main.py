"""Initializing the FastAPI application"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from backend.api.authentication.Microsoft import AUTHENTICATION_SERVER
from backend.api.routes.web import web_router
from backend.api.routes.openai import openai_router
from backend.api.routes.upload import upload_router

# Set up FastAPI settings
app = FastAPI()

app.include_router(web_router)
app.include_router(openai_router)
app.include_router(AUTHENTICATION_SERVER.router)
app.include_router(upload_router)

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
    max_age=600
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("MS_SECRET"),
)

if os.getenv("environment") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)