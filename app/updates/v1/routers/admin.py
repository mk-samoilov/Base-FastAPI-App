"""
Admin router for v1.
"""

from fastapi import APIRouter

from app.core.database import create_tables, drop_tables


router = APIRouter(prefix="/admin", tags=["Administration"])


@router.post("/setup_database", summary="Setup database")
async def setup_database():
    """Drop and recreate all database tables."""
    await drop_tables()
    await create_tables()
    return {"success": True, "msg": "Database has been setup successfully"}
