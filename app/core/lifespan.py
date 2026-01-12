import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .updates_engine import initialize_updates
from .database import init_database, get_session_factory
from .hooks import registry

from app.common.rate_limiter import get_redis


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application lifespan handler."""

    redis = get_redis()
    await redis.ping()

    logger.info("Redis connected")

    init_database()
    session_factory = get_session_factory()
    initialize_updates(session_factory)

    for prefix, router in registry.routers.items():
        application.include_router(router)
        logger.debug(f"Included router from update: {prefix}")

    yield

    await redis.aclose()
