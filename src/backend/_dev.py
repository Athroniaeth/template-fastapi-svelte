from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI, Request
from jinja2 import Template
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

from backend import TEMPLATES_PATH, VITE_DEV_SERVER
from backend._vite import get_template_response

# Create a global HTTP client to reuse connections
client: Optional[httpx.AsyncClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create and close the global HTTP client."""
    global client
    client = httpx.AsyncClient(http2=True, follow_redirects=True)
    yield
    await client.aclose()


# Create the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=TEMPLATES_PATH)


@app.get("/")
async def index(request: Request):
    render_html = get_template_response(
        templates,
        template_name="index.jinja2",
        entry_point="src/main.ts",
        is_development=True,
        request=request,
        dict_response={
            "name": "Hello World!",
        },
    )

    return StreamingResponse(content=render_html, media_type="text/html")


@app.get("/{full_path:path}")
async def proxy_request(request: Request, full_path: str):
    # Prepare the headers excluding those that may cause issues
    headers = dict(request.headers)

    # Build destination URL preserving the path and query params
    url = f"{VITE_DEV_SERVER}/{full_path}"
    params = request.query_params

    # Fetch the response from Vite using the global client
    response = await client.get(url, params=params, headers=headers, timeout=None)

    # Inject the auto-reload script in the HTML if the URL targets an HTML file
    if url.endswith((".html", ".htm", "/")):
        content = await response.aread()
        html_text = content.decode("utf-8")
        template = Template(html_text)
        render_html = template.render({"name": "Hello World!"})
        return StreamingResponse(content=render_html, media_type="text/html")

    # Return the response as a streaming response
    return StreamingResponse(
        response.aiter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers),
    )
