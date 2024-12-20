from fastapi import APIRouter, Depends
from src.database.main import get_session
from src.auth.dependencies import get_current_user, AcessTokenBearer
from src.database.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from .schema import CreateReviewSchema, ReviewSchema

review_service = ReviewService()
review_router = APIRouter()


@review_router.post("/book/{book_uid}")#, response_model=ReviewSchema)
async def create_review_for_book(
    book_uid: str,
    review_data: CreateReviewSchema,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.create_book_review(
        user_email=user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session
    )
    # print(user.email)
    # print(book_uid)
    # print(review_data.model_dump())
    return new_review
