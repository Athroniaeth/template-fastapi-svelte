import logging

from src.app.cli import cli


def main() -> None:
    """Main entry point of the app."""
    try:
        cli()
    except Exception as e:
        logging.error(e)
        raise e
        exit(1)
    except KeyboardInterrupt:
        logging.info("User interrupted the program.")
        exit(0)
    else:
        logging.info("Program executed successfully.")

    exit(0)


if __name__ == "__main__":
    main()
