from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse

class User(HTTPEndpoint):
    async def get(self, request):
        username = request.path_params['username']
        return PlainTextResponse(f"Hello, {username}")

