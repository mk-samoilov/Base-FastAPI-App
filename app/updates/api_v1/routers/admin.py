"""
Admin router for api_v1.
"""

from fastapi import APIRouter, Depends

from app.core.database import create_tables, drop_tables

from app.common.rate_limiter import rate_limiter_high_lvl


router = APIRouter(prefix="/api/v1/admin", tags=["Administration"])


@router.post("/setup_database", summary="Setup database", dependencies=[Depends(rate_limiter_high_lvl)])
async def setup_database():
    """Drop and recreate all database tables."""

    await drop_tables()
    await create_tables()

    return {"success": True, "msg": "Database has been setup successfully"}
