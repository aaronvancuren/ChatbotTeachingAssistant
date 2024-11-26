from fastapi import Request
from fastapi_msal import MSALAuthorization, MSALClientConfig
from fastapi_msal.models import AuthToken

client_config = MSALClientConfig()
msal_auth = MSALAuthorization(client_config)

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
        context.update({"logged_in": True})
    return context
