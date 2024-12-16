from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from uuid import UUID, uuid4
from typing import Optional
class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    uid: UUID = Field(
        sa_column=Column(
         pg.UUID,
         nullable=False,
         primary_key=True,
         default=uuid4
        )
    )
    title: str
    author: str
    genre: str
    year: int
    language: str
    user_uid : Optional[UUID] = Field(
        default=None,
        foreign_key="users.uid"
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, default=datetime.now
        )
    ) 
    
    def __repr__(self):
        return f"<Book {self.title}>"