"""
Patch 2026-01 - Example patch demonstrating priority override.

This patch:
- Overrides get_all_books service with higher priority (adds sorting)
- Adds new /stats router
"""

from app.core.hooks import hookimpl


class UpdatePlugin:
    """Patch plugin demonstrating granular priority override."""

    @hookimpl
    def register_services(self, session_factory):
        """Override get_all_books with sorting (priority 2 > 1)."""
        from .services import get_all_books_sorted
        return {
            # Override v1's get_all_books with priority 2
            "get_all_books": (2, get_all_books_sorted),
        }

    @hookimpl
    def register_routers(self):
        """Add new stats router."""
        from .routers import stats
        return {
            "/stats": (1, stats.router),
        }
