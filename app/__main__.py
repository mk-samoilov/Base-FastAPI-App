"""Entry point for running as module: python -m app"""

import uvicorn

from app.config import settings


if __name__ == "__main__":
    uvicorn.run(
        app="app.core:app",
        host=settings.host,
        port=settings.port,
        reload=settings.auto_reload
    )
