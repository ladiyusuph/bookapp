from pydantic import BaseModel
from sqlmodel import Field
from datetime import datetime
import uuid

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(max_length=9)
    email : str = Field(max_length=40)
    password : str = Field(min_length=6)
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password:str = Field(exclude=True)
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 