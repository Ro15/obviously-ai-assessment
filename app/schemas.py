from pydantic import BaseModel, Field
from datetime import date

class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date
    summary: str | None = None
    genre: str | None = None

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    published_date: date | None = None
    summary: str | None = None
    genre: str | None = None

class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True
