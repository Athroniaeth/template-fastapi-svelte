from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend import DIST_PATH

# Create the FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory=DIST_PATH)
app.mount("/assets", StaticFiles(directory=DIST_PATH / "assets"), name="assets")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "name": "Hello World!"}
    )
