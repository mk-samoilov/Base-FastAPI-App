"""
Frontend pages router.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config import settings
from app.core.templates import get_templates
from app.core.hooks import registry
from app.core.database import SessionDep


router = APIRouter(tags=["Frontend"])
templates = get_templates()


@router.get(path="/", response_class=HTMLResponse, summary="Home page")
async def home(request: Request):
    """Render home page."""

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "settings": settings}
    )


@router.get(path="/about", response_class=HTMLResponse, summary="About page")
async def about(request: Request):
    """Render about page."""

    return templates.TemplateResponse(
        "about.html",
        {"request": request, "settings": settings}
    )


@router.get(path="/books", response_class=HTMLResponse, summary="Books page")
async def books_page(request: Request, session: SessionDep):
    """Render books page with list of all books."""

    get_all_books = registry.get_service("get_all_books")

    if get_all_books:
        books = await get_all_books(session)
    else:
        books = []

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "settings": settings,
            "books": books
        }
    )
