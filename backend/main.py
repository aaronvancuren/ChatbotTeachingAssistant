"""Initializing the FastAPI application"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_msal import MSALAuthorization, MSALClientConfig
from fastapi.staticfiles import StaticFiles

from backend.api.routes.web import web_router
from backend.api.routes.openai import openai_router

#
client_config = MSALClientConfig()
msal_auth = MSALAuthorization(client_config)

# Set up FastAPI settings
app = FastAPI()

#
app.include_router(web_router)
app.include_router(openai_router)
app.include_router(msal_auth.router)

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
