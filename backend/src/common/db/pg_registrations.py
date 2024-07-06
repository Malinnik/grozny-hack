from loguru import logger
from sqlalchemy import delete, insert, select, update
from annotations.objects import RegistrationAddDTO
from core.orm import RegistrationsModel
from core.services import services

async def add_registration(registration: RegistrationAddDTO):
    query = insert(RegistrationsModel).values(registration.to_dict()).returning(RegistrationsModel)


    async with services['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e
        

async def delete_registration(registration_id: int):
    
    query = delete(RegistrationsModel).where(RegistrationsModel.id == registration_id).returning(RegistrationsModel.id)

    async with services['db_engine'].begin() as session:
       try:
           result = await session.execute(query)
           return result.first()
       except Exception as e:
           logger.error(e)
           raise e
       
async def get_registration(registration_id: int):
    query  = select(RegistrationsModel).where(RegistrationsModel.id == registration_id)

    async with services['db_engine'].begin() as session:
        try:
            result  = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e

async def get_all_registrations():
    query  = select(RegistrationsModel)
    async with services['db_engine'].begin() as session:
        try:
            result  = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e







