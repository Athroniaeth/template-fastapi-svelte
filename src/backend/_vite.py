import json
import logging
from functools import partial
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from backend import MANIFEST_PATH, VITE_DEV_SERVER, TEMPLATES_PATH


def get_template_vite(
    dev_mode: bool,
    path: Path = TEMPLATES_PATH,
) -> Jinja2Templates:
    """Get the Jinja2 templates object with Vite assets."""
    logging.info(f"Development mode: {dev_mode}")

    templates = Jinja2Templates(directory=path)
    templates.env.globals["asset"] = partial(vite_asset, is_development=dev_mode)

    return templates


def get_template_response(
    templates: Jinja2Templates,
    template_name: str = "index.jinja2",
    entry_point: str = "src/main.ts",
    is_development: bool = False,
    request: Optional[Request] = None,
    dict_response: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Render a Jinja2 template and return an HTML response.

    Notes:
        This function replace the templates.TemplateResponse from FastAPI, allowing
        to use Vite / FastAPI / Jinja2 stack. (With development or production mode)

    Args:
        templates (Jinja2Templates): Jinja2 templates object.
        template_name (str): Name of the file Jinja2 template.
        entry_point (str): Entry point of the Vite application.
        is_development (bool): Flag to use Vite development server.
        request (Optional[Request]): FastAPI request object.
        dict_response (Optional[Dict[str, Any]]): Dictionary with the response data for the template.

    Returns:
        str: Rendered HTML response.
    """
    if dict_response is None:
        dict_response = {"request": request} if request else {}

    template = templates.get_template(template_name)
    rendered_html = template.render(dict_response)

    # fmt: off
    if is_development:
        rendered_html += f'\n\n<script type="module" src="{VITE_DEV_SERVER}/@vite/client"></script>'
        rendered_html += f'\n\n<script type="module" src="{VITE_DEV_SERVER}/{entry_point}"></script>'
    else:
        rendered_html += parse_manifest(entry_key=entry_point)

    return rendered_html


def parse_manifest(entry_key: str = "src/main.ts") -> str:
    """Parse the manifest Vite and return the HTML tags for the entry."""
    content = MANIFEST_PATH.read_text("utf-8")
    manifest_data = json.loads(content)

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


def check_vite_running():
    """Check if the Vite development server is running."""
    logging.info("Checking if Vite development server is running...")

    try:
        requests.get(VITE_DEV_SERVER, timeout=0.1)
    except requests.exceptions.ConnectionError:
        raise ValueError(
            "Vite development server is not running. Please use `npm run dev` to start it."
        )


def vite_asset(asset_path: str, is_development: bool = False) -> str:
    """
    Return the URL of an asset, either from the Vite dev server or manifest.

    Args:
        asset_path (str): The path of the asset.
        is_development (bool): Whether to use the Vite dev server or manifest.

    Returns:
        str: The URL of the asset (either on the Vite dev server or manifest).
    """
    if is_development:
        # En dev, on renvoie directement l'URL du serveur de Vite
        return f"{VITE_DEV_SERVER}/{asset_path}"
    else:
        # En production, on lit le manifest généré par Vite
        return asset_path[3:]  # Remove the "src" prefix
