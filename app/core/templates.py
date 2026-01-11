"""
Templates helper for Jinja2 templating.
"""

from functools import lru_cache
from fastapi.templating import Jinja2Templates


@lru_cache
def get_templates() -> Jinja2Templates:
    """
    Get global Jinja2 templates instance.

    Returns:
        Jinja2Templates: Templates instance for rendering HTML
    """
    return Jinja2Templates(directory="templates")
