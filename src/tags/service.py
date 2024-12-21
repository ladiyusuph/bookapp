from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.database.models import Tag
from .schema import TagCreateSchema


class TagService:

    async def create_tag(
        self, book_uid: str, tag_text: TagCreateSchema, session: AsyncSession
    ):
        tag = Tag(**tag_text.model_dump())

        session.add(tag)

        await session.commit()

        return tag

    async def get_tag_by_id(self, tag_uid: str, session: AsyncSession):
        tag = select(Tag).where(Tag.uid == tag_uid)
        result = await session.exec(tag)
        if result:
            return result.first()
        else:
            return None

    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        tag = await self.get_tag_by_id(tag_uid, session)
        if tag:
            await session.delete(tag)
            await session.commit()
            return True
        else:
            return False

    async def update_tag(
        self, tag_uid: str, update_txt: TagCreateSchema, session: AsyncSession
    ):
        tag = await self.get_tag_by_id(tag_uid, session)
        if tag:
            update_data_dict = update_txt.model_dump()

            for k, v in update_data_dict.items():
                setattr(tag, k, v)

            await session.commit()
            return tag
        return None

    async def get_all_tags(self, session: AsyncSession):
        tags = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(tags)

        if result:
            return result.all()

        return None
