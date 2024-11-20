from fastapi import Request
from fastapi_msal import MSALAuthorization, MSALClientConfig
from fastapi_msal.models import AuthToken

client_config = MSALClientConfig()
msal_auth = MSALAuthorization(client_config)

async def get_context(request: Request):
    token: AuthToken = await msal_auth.handler.get_token_from_session(request)
    context: dict = {"logged_in": False}
    if(token != None):
        context.update({"id_token": token.id_token})
        context.update({"logged_in": True})
    return context
