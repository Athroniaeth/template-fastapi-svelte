import httpx
from fastapi import FastAPI, Request
from jinja2 import Template
from starlette.responses import StreamingResponse

app = FastAPI()

# Adresse de votre serveur de développement Vite (modifiez si besoin)
VITE_DEV_SERVER = "http://localhost:5175/"

# Créer un client HTTP global pour réutiliser les connexions
client: httpx.AsyncClient = None


@app.on_event("startup")
async def startup_event():
    global client
    client = httpx.AsyncClient(http2=True)  # active HTTP/2 si possible


@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()


@app.get("/{full_path:path}")
async def proxy_request(request: Request, full_path: str):
    # Préparez les en-têtes en excluant ceux qui peuvent poser problème
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("accept-encoding", None)

    # Construisez l'URL de destination en préservant le chemin et les query params
    url = f"{VITE_DEV_SERVER}{full_path}"

    # Récupération de la réponse depuis Vite en utilisant le client global
    response = await client.get(url, params=request.query_params, headers=headers, timeout=None)

    if url.endswith((".html", ".htm", "/")):
        # Injecter le script de rechargement automatique dans le HTML
        content = await response.aread()
        html_text = content.decode("utf-8")
        template = Template(html_text)
        render_html = template.render({"name": "Vite"})
        return StreamingResponse(content=render_html, media_type="text/html")

    # Retourner la réponse en streaming
    return StreamingResponse(
        response.aiter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers),
    )
