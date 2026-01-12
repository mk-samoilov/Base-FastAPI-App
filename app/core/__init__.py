"""
FastAPI application with plugin-based updates system.
"""

import logging

from fastapi import FastAPI

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


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""

    return {
        "app": settings.app_title,
        "version": settings.app_version,
        "status": "running",
    }
