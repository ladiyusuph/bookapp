from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from .database import books
from .schema import BookResponse, CreateBook

book_router = APIRouter()
# book_data = books
@book_router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books():
    return books


@book_router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: int) -> dict:
    for id, book in enumerate(books):
        print("id", id)
        if id == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")


@book_router.post("/")
async def create_a_book(book_data: CreateBook) -> dict:
    book = book_data.model_dump()
    books.append(book)

    return book


@book_router.put("/{book_id}")
async def update_book(book_id: int, book_data: CreateBook):
    for id, book in enumerate(books):
        if id == book_id:
            book_update = book_data.model_dump()
            book["author"] = book_update["author"]
            book["title"] = book_update["title"]
            book["genre"] = book_update["genre"]
            book["year"] = book_update["year"]
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")
    


@book_router.delete("/{book_id}")
async def delete_book(book_id: int):
    for id, book in enumerate(books):
        if id == book_id:
            books.remove(book)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")
