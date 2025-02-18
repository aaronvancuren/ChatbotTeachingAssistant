from enum import Flag, auto
import os
from fastapi import Request
from fastapi_msal import MSALAuthorization, MSALClientConfig
from fastapi_msal.models import AuthToken, TokenStatus

client_config = MSALClientConfig()
msal_auth = MSALAuthorization(client_config)

class ACCESS_REQUIRED(Flag):
    LOGIN = auto() 
    ADMIN = auto()

async def get_context(request: Request):
    """
    Gets the user's token from the current session through Microsoft Authentication
    Args:
        request: this is the page request
    Returns:
        dict: contains a logged_in boolean value and IDTokenClaims
    """
    token: AuthToken = await msal_auth.handler.get_token_from_session(request)
    context: dict = {"logged_in": False}
    if(token != None):
        context.update({"id_token": token.id_token})
        context.update({"logged_in": token.id_token_claims.validate_token() == TokenStatus.VALID})
    return context

async def validate_user(request: Request, Access_Req: ACCESS_REQUIRED = ACCESS_REQUIRED.LOGIN):
    """
    Validates the user's token from the current session through Microsoft Authentication
    Args:
        request: this is the page request
        Access_Req: this is the required access level for the user
    Returns:
        bool: True if the user is validated, False otherwise
    """
    token: AuthToken = await msal_auth.handler.get_token_from_session(request)
    if(token != None):
        if(token.id_token_claims.validate_token() == TokenStatus.VALID):
            if(Access_Req == ACCESS_REQUIRED.ADMIN):
                return token.id_token_claims.user_id in os.getenv("ADMIN_USERS")
            return True
    return False
