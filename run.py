#!/usr/bin/env python
"""
Run the FastAPI development server for YB Knowledge Factory MVP.

Usage:
    python run.py

Binds 0.0.0.0 so this also works behind a platform-assigned $PORT (e.g.
Zeabur); local dev is unaffected since 0.0.0.0 still answers on localhost.
Falls back to 8000 when PORT isn't set (plain local `python run.py`).
"""

import os

import uvicorn
from pathlib import Path

if __name__ == "__main__":
    app_dir = Path(__file__).parent / "app"
    port = int(os.environ.get("PORT", 8000))

    print("Starting YB Knowledge Factory MVP")
    print(f"App directory: {app_dir}")
    print(f"Server: http://0.0.0.0:{port}")
    print("Press Ctrl+C to stop\n")

    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        app_dir=str(app_dir),
    )
