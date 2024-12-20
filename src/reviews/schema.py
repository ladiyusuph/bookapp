from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ReviewSchema(BaseModel):
    uid: UUID
    rating :int
    review_txt: str
    user_uid : UUID
    book_uid : UUID
    created_at: datetime
    updated_at: datetime


class CreateReviewSchema(BaseModel):
    rating :int
    review_txt: str