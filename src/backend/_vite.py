import json
from typing import Optional, Dict, Any

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from backend import MANIFEST_PATH, VITE_DEV_SERVER


def get_template_response(
    templates: Jinja2Templates,
    template_name: str = "index.jinja2",
    entry_point: str = "src/main.ts",
    is_development: bool = False,
    request: Optional[Request] = None,
    dict_response: Optional[Dict[str, Any]] = None,
) -> str:
    """Render a Jinja2 template (in Vite / FastAPI / Jinja2 stack) and return an HTML response."""
    if dict_response is None:
        dict_response = {"request": request} if request else {}

    template = templates.get_template(template_name)
    rendered_html = template.render(dict_response)

    if is_development:
        rendered_html += (
            f'\n\n<script type="module" src="{VITE_DEV_SERVER}/@vite/client"></script>'
        )
        rendered_html += (
            f'\n\n<script type="module" src="{VITE_DEV_SERVER}/main.ts"></script>'
        )
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
