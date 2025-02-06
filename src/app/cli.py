from typer import Typer

cli = Typer()


@cli.command()
def run(
    source: str = "src.app.app:app",
    host: str = "localhost",
    port: int = 8000,
):
    """Run the FastAPI application."""
    import uvicorn
    uvicorn.run(source, host=host, port=port)
