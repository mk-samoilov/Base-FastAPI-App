"""
Frontend api_v1 update - HTML pages with Jinja2 templates.

This update adds:
- Home page (/home)
- About page (/about)
- Books page with UI (/books)
"""

from app.core.hooks import hookimpl


class UpdatePlugin:
    """Frontend plugin for HTML pages."""

    @hookimpl
    def register_routers(self):
        """Register frontend routers."""
        from .routers import pages
        return {
            "": (1, pages.router)
        }
