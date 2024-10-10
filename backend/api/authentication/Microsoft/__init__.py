from fastapi_msal import MSALAuthorization, MSALClientConfig

from . auth_config import *

auth_client = MSALClientConfig()
auth_client.client_id = CLIENT_ID
auth_client.client_credential = CLIENT_SECRET
auth_client.tenant = TENANT
auth_client.login_path = LOGIN_PATH
auth_client.redirect_uri = REDIRECT_PATH
auth_client.logout_path = LOGOUT_PATH

AUTHENTICATION_SERVER = MSALAuthorization(client_config=auth_client)
