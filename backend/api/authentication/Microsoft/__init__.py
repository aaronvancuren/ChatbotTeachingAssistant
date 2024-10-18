from fastapi import Request
from fastapi_msal import MSALAuthorization, MSALClientConfig

import msal

from . auth_config import *

AUTHENTICATION_CLIENT = MSALClientConfig()
AUTHENTICATION_CLIENT.client_id = CLIENT_ID
AUTHENTICATION_CLIENT.client_credential = CLIENT_SECRET
AUTHENTICATION_CLIENT.tenant = TENANT
AUTHENTICATION_CLIENT.login_path = LOGIN_PATH
AUTHENTICATION_CLIENT.redirect_uri = REDIRECT_PATH
AUTHENTICATION_CLIENT.logout_path = LOGOUT_PATH

AUTHENTICATION_SERVER = MSALAuthorization(client_config=AUTHENTICATION_CLIENT)

async def get_user_context(Request: Request):
    """
    Constructs the authentication context of the currently logged in user
    Args:
        request: the data contained in the request that the server received
    
    Returns:
        Attempts to get the session token of the current authentication session.
        If the user is not logged in, it returns a default object.
        If the user is logged in, returns user context information such as name and ID.
    """
    token = await AUTHENTICATION_SERVER.get_session_token(request=Request)
    if not token or not token.id_token_claims:
        context = {
            "user": '',
            "user_id": None,
            "version": msal.__version__,
            "loggedin": 'false',
        }   
    else:
        context = {
            "user": token.id_token_claims.display_name,
            "user_id": token.id_token_claims.user_id,
            "version": msal.__version__,
            "loggedin": 'true',
        }
    return context