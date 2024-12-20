from src.books.services import BookService
from src.auth.services import UserService
from src.database.models import Review
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schema import CreateReviewSchema


book_service = BookService()
user_service = UserService()

class ReviewService:
    
    async def create_book_review(self, user_email:str, book_uid:str, review_data:CreateReviewSchema, session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)
            # print(book)
            # print(user)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found !!!!"
                )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found !!!"
                )
            new_review = Review(
                **review_data.model_dump()
            )
            # print(new_review)
            # print("---------------------")
            new_review.user_uid = user.uid
            new_review.book_uid = book.uid
            print(new_review)
            # print("-------------------------")
            session.add(new_review)
            
            await session.commit()
            
            return new_review
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ooops... An error occured"
            )