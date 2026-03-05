"""Script to run the FastAPI server."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
