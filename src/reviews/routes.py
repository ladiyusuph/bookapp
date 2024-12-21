from fastapi import APIRouter, Depends, status
from src.database.main import get_session
from src.auth.dependencies import get_current_user, AcessTokenBearer
from src.database.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from .schema import CreateReviewSchema, ReviewSchema
from typing import List


review_service = ReviewService()
review_router = APIRouter()


@review_router.post("/book/{book_uid}", response_model=ReviewSchema)
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


@review_router.get("/user/{user_uid}", response_model=List[ReviewSchema])
async def get_user_reviews(
    user_uid:str,
    session:AsyncSession = Depends(get_session),
    _:User = Depends(get_current_user)
):
    user_reviews = await review_service.get_all_users_reviews(
        user_uid, session
    )
    
    return user_reviews

@review_router.get("/{review_uid}", response_model=ReviewSchema)
async def get_review_by_id(
    review_uid:str,session:AsyncSession=Depends(get_session),
    _:User = Depends(get_current_user)
    ):
    book = await review_service.get_review_by_id(review_uid, session)
    
    return book

