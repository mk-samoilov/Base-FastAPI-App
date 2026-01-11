"""
Books router for api_v1.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.core.database import SessionDep
from app.core.hooks import registry

from app.common.rate_limiter import (
    rate_limiter_low_lvl,
    rate_limiter_medium_lvl # ,
    # rate_limiter_high_lvl
)


router = APIRouter(prefix="/api/v1/books", tags=["Books API"])


@router.get("", summary="Get all books", dependencies=[Depends(rate_limiter_low_lvl)])
async def get_books(session: SessionDep):
    """Get all books."""

    get_all_books = registry.get_service("get_all_books")
    books = await get_all_books(session)

    return books


@router.get("/{book_id}", summary="Get book by ID", dependencies=[Depends(rate_limiter_low_lvl)])
async def get_book(book_id: int, session: SessionDep):
    """Get book by ID."""

    get_book_by_id = registry.get_service("get_book_by_id")
    book = await get_book_by_id(session, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("", summary="Create book", dependencies=[Depends(rate_limiter_medium_lvl)])
async def create_book(session: SessionDep, title: str, author: str):
    """Create a new book."""

    book_add_schema = registry.get_schema("BookAddSchema")
    data = book_add_schema(title=title, author=author)

    create_book_func = registry.get_service("create_book")
    book = await create_book_func(session, data.title, data.author)

    return {"success": True, "book_id": book.id}
