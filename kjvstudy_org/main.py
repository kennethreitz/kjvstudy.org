import uvicorn
from .server import app


def main():
    """Main entry point for the KJV Study application."""
    uvicorn.run(
        "kjvstudy_org.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()