from typing import Tuple
from loguru import logger
from sqlalchemy import Row, insert, select
from annotations.objects import ImageAddDTO
from core.orm import ImagesModel
from core.services import services, AsyncEngine

async def add_image_to_db(image: ImageAddDTO) -> Row[Tuple[ImagesModel]] | None:
    query = insert(ImagesModel).values(image.to_dict()).returning(ImagesModel)

    async with services['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e

async def get_image_path(id: int) -> Row[Tuple[str, str]] | None:
    query = select(ImagesModel.bucket, ImagesModel.path).where(ImagesModel.id == id)

    async with services['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e
        
async def get_images_ids(page: int, page_size: int = 9)  -> list[ImageAddDTO]:
    if page > 1:
        query  = select(ImagesModel.id).offset(page * page_size).limit(page_size).order_by(ImagesModel.created_at)
    else:
        query  = select(ImagesModel.id).offset(0).limit(page_size).order_by(ImagesModel.created_at)

    async with services['db_engine'].begin() as session:
        try:
            result  = await session.execute(query)
            return result
        except Exception as e:
            logger.error(e)
            raise e

async def get_max_pages(page_size: int  =  9) -> int:
    query = select(ImagesModel.id).order_by(ImagesModel.created_at)
    
    async with services['db_engine'].begin() as session:
        try:
            result   = await session.execute(query)
            return result.rowcount // page_size
        except Exception as e:
            logger.error(e)
            raise e


