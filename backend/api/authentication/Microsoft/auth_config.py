import os
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

### Source: https://registeredapps.hosting.portal.azure.net/registeredapps/Content/1.0.2818.1081/Quickstarts/en/PythonQuickstartPage.html

# Application (client) ID of app registration
CLIENT_ID = os.getenv("MS_ID")

# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("MS_SECRET")
TENANT = os.getenv('MS_TENANT')
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('MS_TENANT')}"

REDIRECT_PATH = os.getenv('MS_REDIRECT') # Used for forming an absolute URL to your redirect URI.
                                         # The absolute URL must match the redirect URI you set
                                         # in the app's registration in the Azure portal.
LOGIN_PATH = os.getenv('MS_LOGIN')
LOGOUT_PATH = os.getenv('MS_LOGOUT')
# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/me'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.Read"]

ACCOUNT_LOGGED_IN = False