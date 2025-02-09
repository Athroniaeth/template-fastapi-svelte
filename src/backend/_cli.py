import logging
import os

from typer import Typer

from backend._vite import check_vite_running

cli = Typer(
    help="CLI for the FastAPI application.",
    add_completion=False,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


@cli.command()
def run(
    source: str = "backend._app:app",
    host: str = "localhost",
    port: int = 8000,
    dev_mode: bool = False,
):
    """Run the FastAPI application."""
    import uvicorn

    check_vite_running() if dev_mode else ...
    os.environ["DEV_MODE"] = "true" if dev_mode else "false"
    logging.info(f"Running FastAPI application at http://{host}:{port}")
    uvicorn.run(source, host=host, port=port)


@cli.command()
def hello_world():
    """Fake command for force Typer to list commands."""
    ...
