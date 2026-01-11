"""
SQLAlchemy models for api_v1.
"""

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BookModel(Base):
    """Book model."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
