"""
SkillAdapt - Root Application Entrypoint
Exposes the FastAPI 'app' at the root level for cloud platforms (e.g. Render, Railway)
executing 'uvicorn main:app --host 0.0.0.0 --port $PORT'.
"""

import os
import sys

# Ensure backend directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the core application from backend/main.py
from backend.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"[INFO] Launching SkillAdapt from root main.py on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=False)
