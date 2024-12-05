from pydantic import BaseModel

class CreateBook(BaseModel):
    title: str
    author: str
    genre: str
    year: int


class BookResponse(BaseModel):
    title: str
    author: str
    genre: str
    year: int
