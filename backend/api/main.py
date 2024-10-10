"""docstring"""
from fastapi import APIRouter

from backend.api.routes import ai

ai_router = APIRouter()
ai_router.include_router(ai.router)
