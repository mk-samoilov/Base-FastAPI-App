"""
Update api_v1 - Base implementation.
"""

from app.core.hooks import hookimpl


class UpdatePlugin:
    """Base update plugin for api_v1."""

    @hookimpl
    def register_models(self):
        """Register api_v1 database models."""

        from .models import BookModel

        return {"BookModel": (1, BookModel)}

    @hookimpl
    def register_schemas(self):
        """Register api_v1 Pydantic schemas."""

        from .schemas import BookAddSchema, BookSchema

        return {
            "BookAddSchema": (1, BookAddSchema),
            "BookSchema": (1, BookSchema),
        }

    @hookimpl
    def register_services(self, session_factory):
        """Register api_v1 service functions."""

        from .services import get_all_books, create_book, get_book_by_id

        return {
            "get_all_books": (1, get_all_books),
            "create_book": (1, create_book),
            "get_book_by_id": (1, get_book_by_id),
        }

    @hookimpl
    def register_routers(self):
        """Register api_v1 API routers."""

        from .routers import books, admin

        return {
            "/books": (1, books.router),
            "/admin": (1, admin.router),
        }
