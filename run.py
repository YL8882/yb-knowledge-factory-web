#!/usr/bin/env python
"""
Run the FastAPI development server for YB Knowledge Factory MVP.

Usage:
    python run.py

The server will start at http://localhost:8000
"""

import uvicorn
from pathlib import Path

if __name__ == "__main__":
    app_dir = Path(__file__).parent / "app"

    print("Starting YB Knowledge Factory MVP")
    print(f"App directory: {app_dir}")
    print("Server: http://localhost:8000")
    print("Press Ctrl+C to stop\n")

    # Run the server
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=str(app_dir),
    )
