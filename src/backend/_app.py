from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend import DIST_PATH, TEMPLATES_PATH
from backend._vite import get_template_response

# Create the FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES_PATH)
app.mount("/assets", StaticFiles(directory=DIST_PATH / "assets"), name="assets")


@app.get("/")
def index(request: Request):
    response = get_template_response(
        templates,
        template_name="index.jinja2",
        entry_point="src/main.ts",
        request=request,
        dict_response={
            "name": "Hello World!",
        },
    )
    return HTMLResponse(content=response, status_code=200)
