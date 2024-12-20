from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.database.models import Book
from .schema import CreateBook


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)

        return result.all()

    async def get_user_books(self, user_uid:str, session:AsyncSession):
        statment = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statment)
        
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        return result.first()

    async def create_book(self, book_data: CreateBook, user_uid:str, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        new_book.user_uid = user_uid
        # year_int =
        # new_book.year = datetime.strptime(book_data_dict["year"], "%Y")
        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: CreateBook, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update:
            update_data_dict = update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update
        return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return None
