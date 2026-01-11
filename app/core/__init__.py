"""
FastAPI application with plugin-based updates system.
"""

import logging

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings

from .lifespan import lifespan


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

# Mount static files
static_path = Path("static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"Static files mounted at /static from {static_path}")
else:
    logger.warning(f"Static directory not found: {static_path}")


#@app.get("/", tags=["Root"])
#async def root():
#    """Root endpoint."""

#    return {
#        "app": settings.app_title,
#        "version": settings.app_version,
#        "status": "running",
#    }
