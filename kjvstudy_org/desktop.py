"""Desktop application entry point for KJV Study.

This module provides a standalone entry point for the desktop application,
configured to run on a non-standard port (31102 - the number of verses in the KJV).
"""

import os
import sys


def main():
    """Start the KJV Study server for desktop use."""
    import uvicorn

    # Get port from environment or use default (31102 = number of KJV verses)
    port = int(os.environ.get("KJVSTUDY_PORT", "31102"))
    host = os.environ.get("KJVSTUDY_HOST", "127.0.0.1")

    # Determine the base directory for resources
    if getattr(sys, "frozen", False):
        # Running as bundled executable (PyInstaller)
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Change to base directory so relative paths work
    os.chdir(base_dir)

    print(f"Starting KJV Study server on {host}:{port}")
    print(f"Base directory: {base_dir}")

    uvicorn.run(
        "kjvstudy_org.server:app",
        host=host,
        port=port,
        log_level="warning",
        # Disable reload in production
        reload=False,
    )


if __name__ == "__main__":
    main()
