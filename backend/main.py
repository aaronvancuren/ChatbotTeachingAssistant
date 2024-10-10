"""" update docstring """

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.main import ai_router

# Set up FastAPI settings
app = FastAPI()

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ORIGINS")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)
