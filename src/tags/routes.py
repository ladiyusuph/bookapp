from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import get_current_user
from src.database.main import get_session
from src.database.models import User
from .service import TagService
from .schema import TagResponseSChema, TagCreateSchema
from typing import List
import logging

tag_router = APIRouter()
tag_service = TagService()


@tag_router.get("/", response_model=List[TagResponseSChema])
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    try:
        tags = await tag_service.get_all_tags(session=session)

        if tags:
            return tags
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No tags found"
            )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="An Error occured"
        )


@tag_router.post("/create/{book_uid}", response_model=TagResponseSChema)
async def create_tag(
    tag_data: TagCreateSchema,
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user),
):
    try:
        new_tag = await tag_service.create_tag(book_uid, tag_data, session)

        if new_tag:
            return new_tag
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="An Error occured"
        )


@tag_router.get("/{tag_uid}", response_model=TagResponseSChema)
async def get_tag_by_id(tag_uid:str, session:AsyncSession=Depends(get_session), _:User=Depends(get_current_user)):
    try:
        tag = await tag_service.get_tag_by_id(tag_uid, session)
        if tag:
            return tag
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="An Error occured"
        )
        
        
@tag_router.post("/update/{tag_uid}", response_model=TagResponseSChema)
async def update_tag(update_txt:TagCreateSchema, tag_uid:str, session:AsyncSession=Depends(get_session), _:User=Depends(get_current_user)):
    try:
        updated_tag = await tag_service.update_tag(tag_uid, update_txt, session)
        
        if updated_tag:
            return updated_tag
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="An Error occured"
        )    


@tag_router.delete("/delete/{tag_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_uid:str, session:AsyncSession=Depends(get_session), _:User = Depends(get_current_user)):
    try:
        deleted = await tag_service.delete_tag(tag_uid, session)
        if deleted:
            return None
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="An Error occured"
        )   