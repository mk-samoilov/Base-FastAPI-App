"""
Service functions for api_v1.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BookModel


async def get_all_books(session: AsyncSession) -> list[BookModel]:
    """Get all books from database."""
    query = select(BookModel)
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_book_by_id(session: AsyncSession, book_id: int) -> BookModel | None:
    """Get book by ID."""
    query = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_book(session: AsyncSession, title: str, author: str) -> BookModel:
    """Create a new book."""
    book = BookModel(title=title, author=author)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book
