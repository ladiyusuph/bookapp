from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

class CreateBook(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    language: str


class BookResponse(BaseModel):
    uid: UUID
    title: str
    author: str
    genre: str
    year: int
    language: str
    created_at: datetime
    updated_at: datetime
