import os
import uvicorn
from .server import app


def main():
    """Main entry point for the KJV Study application."""
    workers = int(os.getenv("WORKERS", "4"))

    uvicorn.run(
        "kjvstudy_org.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
        workers=workers
    )


if __name__ == "__main__":
    main()