import os
from .server import app


def main():
    """Main entry point for the KJV Study application."""
    app.run(
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
