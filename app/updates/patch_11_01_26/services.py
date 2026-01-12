"""
Service functions for patch_11_01_26.
Demonstrates overriding v1 services with higher priority.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.updates.v1.models import BookModel


async def get_all_books_sorted(session: AsyncSession) -> list[BookModel]:
    """
    Get all books from database, sorted by title.

    This overrides v1's get_all_books (priority 2 > 1).
    """
    query = select(BookModel).order_by(BookModel.title)
    result = await session.execute(query)
    return list(result.scalars().all())
