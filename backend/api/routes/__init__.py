from fastapi import Request
from fastapi_msal import MSALAuthorization, MSALClientConfig
from fastapi_msal.models import AuthToken, TokenStatus

from backend.database.database_class_sections import get_user_classes
from backend.database.database_user_conversations import get_user_conversations

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
        context.update({"logged_in": True})
        context.update({"id_token": token.id_token})
        context.update({"id": token.id_token_claims.user_id})
        context.update({"preferred_name": token.id_token_claims.preferred_username})
        context.update({"display_name": token.id_token_claims.display_name})
        context.update({"email": token.id_token_claims.email})
        context.update({"class_list": get_user_classes(token.id_token_claims.user_id)}) #TODO update method of getting student classes
        context.update({"conversation_list": get_user_conversations(token.id_token_claims.user_id)}) #TODO update method of getting conversations for classes. Need to discuss when we should be getting the conversations
    
    return context