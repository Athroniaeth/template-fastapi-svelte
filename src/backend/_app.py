import json
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend import DIST_PATH, MANIFEST_PATH, TEMPLATES_PATH

# Create the FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES_PATH)
app.mount("/assets", StaticFiles(directory=DIST_PATH / "assets"), name="assets")

manifest_data = json.loads(MANIFEST_PATH.read_text("utf-8"))


def get_template_response(
    template_name: str = "index.jinja2",
    entry_point: str = "src/main.ts",
    request: Optional[Request] = None,
    dict_response: Optional[Dict[str, Any]] = None,
) -> str:
    """Render a Jinja2 template (in Vite / FastAPI / Jinja2 stack) and return an HTML response."""
    if dict_response is None:
        dict_response = {"request": request} if request else {}

    template = templates.get_template(template_name)
    rendered_html = template.render(dict_response)
    rendered_html += parse_manifest(entry_key=entry_point)

    return rendered_html


def parse_manifest(entry_key: str = "src/main.ts") -> str:
    """Parse the manifest Vite and return the HTML tags for the entry."""
    if entry_key not in manifest_data:
        raise ValueError(f"Entry key '{entry_key}' not found in the manifest file.")

    # Get the entry from the manifest
    entry = manifest_data[entry_key]

    # Inject the CSS files in the head
    css_tags = "\n".join(
        f'<link rel="stylesheet" href="{css_file}" />'
        for css_file in entry.get("css", [])
    )

    # Inject the JS file before the closing body tag
    js_file = f"{entry['file']}"

    # Return the HTML tags
    return f"<script type='module' src='{js_file}'></script>\n{css_tags}"


@app.get("/")
def index(request: Request):
    response = get_template_response(
        "index.jinja2",
        "src/main.ts",
        request, {
            "name": "Hello World!",
        }
    )
    return HTMLResponse(content=response, status_code=200)
