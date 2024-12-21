from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class TagCreateSchema(BaseModel):
    tag_name: str


class TagResponseSChema(TagCreateSchema):
    uid: UUID
    created_at: datetime
    updated_at: datetime
