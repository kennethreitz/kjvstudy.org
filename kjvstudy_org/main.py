import os
from pathlib import Path
from granian import Granian
from .server import api  # noqa: F401


def main():
    """Main entry point for the KJV Study application."""
    workers = int(os.getenv("WORKERS", "4"))
    static_dir = str(Path(__file__).parent / "static")

    granian = Granian(
        "kjvstudy_org.server:api",
        address="0.0.0.0",
        port=8000,
        interface="asgi",
        workers=workers,
        reload=False,
        static_path_route="/static",
        static_path_mount=static_dir,
        static_path_expires=86400,
    )
    granian.serve()


if __name__ == "__main__":
    main()