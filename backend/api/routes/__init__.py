import logging
import uuid

from fastapi import Request
from fastapi_msal import MSALAuthorization, MSALClientConfig
from fastapi_msal.models import AuthToken, TokenStatus

import backend.database.postgres as db
from backend.models import User
from backend.database.database_user_conversations import get_user_conversations

# Configure logging
logging.basicConfig(level=logging.INFO)

client_config = MSALClientConfig()
msal_auth = MSALAuthorization(client_config)

async def get_context(request: Request) -> dict:
    """
    Gets the user's token from the current session through Microsoft Authentication
    Args:
        request: this is the page request
    Returns:
        dict: contains a logged_in boolean value and IDTokenClaims
    """
    context: dict = {"logged_in": False}
    token: AuthToken = await msal_auth.get_session_token(request)
    if token and token.id_token_claims.validate_token() == TokenStatus.VALID:
        email: str = token.id_token_claims.preferred_username
        user: User = db.read_user_by_email(email)
        
        context.update({"conversation_list": get_user_conversations(token.id_token_claims.user_id)})

        # User id will return none if they are a new user. Must save the Microsoft user_id.
        if user.id != uuid.UUID(token.id_token_claims.user_id):
            if db.set_user_id(token.id_token_claims.user_id, email):
                user.id = uuid.UUID(token.id_token_claims.user_id)

        user.courses = user.get_courses()

        context.update({"logged_in": True})
        context.update({"user": user})
        
    return context