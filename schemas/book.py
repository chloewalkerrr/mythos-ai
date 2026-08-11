from datetime import date

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    book_number: int = Field(ge=1)
    publication_date: date | None = None
    isbn: str | None = Field(default=None, max_length=20)
    page_count: int | None = Field(default=None, gt=0)
    summary: str | None = None


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    book_number: int | None = Field(default=None, ge=1)
    publication_date: date | None = None
    isbn: str | None = Field(default=None, max_length=20)
    page_count: int | None = Field(default=None, gt=0)
    summary: str | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    book_number: int
    publication_date: date | None = None
    isbn: str | None = None
    page_count: int | None = None
    summary: str | None = None

    model_config = {
        "from_attributes": True,
    }
