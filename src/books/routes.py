from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from .schema import BookResponse, CreateBook
from src.database.main import get_session
from src.books.services import BookService



book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(session:AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    if books:
        return books
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not Found")

@book_router.get("/{book_uid}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_uid: str, session:AsyncSession=Depends(get_session)):
        
        book = await book_service.get_book(book_uid, session)
        if book:
            return book
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")


@book_router.post("/", response_model = BookResponse)
async def create_a_book(book_data: CreateBook, session:AsyncSession=Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    if new_book:
        return new_book
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error")


@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_data: CreateBook,session:AsyncSession=Depends(get_session)):
    updated_book = await book_service.update_book(book_uid, book_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")
    


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str,session:AsyncSession=Depends(get_session) ):
    book_to_delete = await book_service.delete_book(book_uid,session)
    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")
