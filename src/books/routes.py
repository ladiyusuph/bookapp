from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from .schema import BookResponse, CreateBook, BookDetailResponse
from src.database.main import get_session
from src.books.services import BookService
from src.auth.dependencies import AcessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookService()
user_creds = AcessTokenBearer()
general = Depends(RoleChecker(["admin", "user"]))
admin_only = Depends(RoleChecker(["admin", "user"]))


@book_router.get(
    "/",
    response_model=List[BookResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[general],
)
async def get_books(
    session: AsyncSession = Depends(get_session), credentials=Depends(user_creds)
):
    print(credentials)
    books = await book_service.get_all_books(session)
    if books:
        return books
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Books not Found"
        )


@book_router.get(
    "/user/{user_uid}",
    response_model=List[BookResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[general],
)
async def get_user_books(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    credentials=Depends(user_creds),
):
    print(credentials)
    books = await book_service.get_user_books(user_uid, session)
    if books:
        return books
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Books not Found"
        )


@book_router.get(
    "/{book_uid}",
    response_model=BookDetailResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[general],
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    credentials=Depends(user_creds),
):

    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found"
        )


@book_router.post("/", response_model=BookResponse, dependencies=[general])
async def create_a_book(
    book_data: CreateBook,
    session: AsyncSession = Depends(get_session),
    credentials=Depends(user_creds),
):
    user_uid = credentials.get("user")["uid"]
    new_book = await book_service.create_book(book_data, user_uid, session)
    if new_book:
        return new_book
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error")


@book_router.patch("/{book_uid}", dependencies=[general])
async def update_book(
    book_uid: str,
    book_data: CreateBook,
    session: AsyncSession = Depends(get_session),
    credentials=Depends(user_creds),
):
    updated_book = await book_service.update_book(book_uid, book_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found"
        )


@book_router.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[general]
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    credentials=Depends(user_creds),
):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found"
        )
