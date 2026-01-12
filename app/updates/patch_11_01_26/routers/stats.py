"""
Stats router - new functionality added by patch.
"""

from fastapi import APIRouter
from sqlalchemy import func, select

from app.core.database import SessionDep
from app.updates.v1.models import BookModel


router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("", summary="Get statistics")
async def get_stats(session: SessionDep):
    """Get database statistics."""
    # Count books
    query = select(func.count(BookModel.id))
    result = await session.execute(query)
    books_count = result.scalar() or 0

    # Count unique authors
    query = select(func.count(func.distinct(BookModel.author)))
    result = await session.execute(query)
    authors_count = result.scalar() or 0

    return {
        "books_count": books_count,
        "authors_count": authors_count,
    }
