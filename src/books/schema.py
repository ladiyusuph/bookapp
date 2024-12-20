from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID
from typing import List
from src.reviews.schema import ReviewSchema
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


class BookDetailResponse(BookResponse):
    reviews :List[ReviewSchema]