from fastapi import APIRouter
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import CreateUser
from src.database.models import User
from .utils import generate_password_hash


class UserService:
    async def get_user_by_email(self,email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)

        user = result.first()
        if user:
            return user
        else:
            return None

    async def create_user(self,user_data: CreateUser, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password = generate_password_hash(user_data_dict["password"])
        
        session.add(new_user)
        await session.commit() 
        
        return new_user