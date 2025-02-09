import logging
import os
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend import DIST_PATH
from backend import TEMPLATES_PATH, VITE_DEV_SERVER
from backend._vite import get_template_response

# Create a global HTTP client to reuse connections
client: Optional[httpx.AsyncClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create and close the global HTTP client."""
    global client
    print("Creating the global HTTP client")
    client = httpx.AsyncClient(http2=True, follow_redirects=True)
    yield
    await client.aclose()


# Create the FastAPI app
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=TEMPLATES_PATH)
dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"
logging.info(f"Development mode: {dev_mode}")


@app.get("/")
def index(request: Request):
    response = get_template_response(
        templates,
        template_name="index.jinja2",
        entry_point="src/main.ts",
        is_development=dev_mode,
        request=request,
        dict_response={
            "name": "Hello World!",
        },
    )
    return HTMLResponse(content=response, status_code=200)


if dev_mode:

    @app.get("/{full_path:path}")
    async def proxy_request(request: Request, full_path: str):
        # Build destination URL preserving the path and query params
        url = f"{VITE_DEV_SERVER}/{full_path}"

        # fmt: off # Fetch the response from Vite using the global client
        response = await client.get(
            url, params=request.query_params, headers=request.headers, timeout=None
        )

        # Return the response as a streaming response
        return StreamingResponse(
            response.aiter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers),
        )
else:
    app.mount("/assets", StaticFiles(directory=DIST_PATH / "assets"), name="assets")
