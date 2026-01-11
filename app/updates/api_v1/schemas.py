"""
Pydantic schemas for api_v1.
"""

from pydantic import BaseModel


class BookAddSchema(BaseModel):
    """Schema for creating a book."""

    title: str
    author: str


class BookSchema(BaseModel):
    """Schema for book response."""

    id: int
    title: str
    author: str

    model_config = {"from_attributes": True}
