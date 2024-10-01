import uvicorn

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from backend import *
from backend.errorpages import not_found
from backend.helpers import validate

# This code is our web page map.
# Root directory is '/', this is defaulted to the 'index.html' page.
# Mount('/static', ...) needs to be present to mount the directory where the pages are.
# When a new page is added, insert it above Mount('/static', ...) and give it
# a descriptive file path.
routes = [

    #### End Points
    
    #### Web Pages
    Route('/', endpoint=homepage),
    Route('/chat', endpoint=chatpage),
    Mount('/static', StaticFiles(directory='frontend'), name='static')

]


app = Starlette(debug=True,routes=routes)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.route("/ask", methods=["POST"])
async def submit(request: Request):
    form_data = await request.body()
    print(form_data.decode())
    return JSONResponse({"chat":await validate(request.headers['X-victor-uid'], form_data.decode())})

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_level="info", reload=True)