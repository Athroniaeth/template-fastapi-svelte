import logging

from typer import Typer

cli = Typer(
    help="CLI for the FastAPI application.",
    add_completion=False,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


@cli.command()
def dev(
    source: str = "src.backend._dev:app",
    host: str = "localhost",
    port: int = 8000,
):
    """Run the FastAPI application with the Vite development server."""
    import uvicorn
    import requests

    logging.info("Checking if Vite development server is running...")

    try:
        requests.get("http://localhost:5173/", timeout=0.1)
    except requests.exceptions.ConnectionError:
        raise ValueError(
            "Vite development server is not running. Please use `npm run dev` to start it."
        )

    uvicorn.run(source, host=host, port=port)


@cli.command()
def run(
    source: str = "src.backend._app:app",
    host: str = "localhost",
    port: int = 8000,
):
    """Run the FastAPI application."""
    import uvicorn

    uvicorn.run(source, host=host, port=port)
