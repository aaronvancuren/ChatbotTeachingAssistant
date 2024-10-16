"""TODO: update docstring"""
from starlette.endpoints import HTTPEndpoint
from fastapi.responses import PlainTextResponse

class User(HTTPEndpoint):
    """TODO: update docstring"""
    async def get(self, request):
        """TODO: update docstring"""
        username = request.path_params['username']
        return PlainTextResponse(f"Hello, {username}")
