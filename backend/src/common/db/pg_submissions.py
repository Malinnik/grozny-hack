







from loguru import logger
from sqlalchemy import delete, insert, select, update
from annotations.objects import SubmissionAddDTO, SubmissionUpdateDTO
from core.orm import SubmissionsModel
from core.services import services, AsyncEngine

async def add_submission(submission: SubmissionAddDTO):
    query = insert(SubmissionsModel).values(submission.to_dict()).returning(SubmissionsModel.id)


    async with services['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e
        

async def delete_submission(submission_id: int):
    
    query = delete(SubmissionsModel).where(SubmissionsModel.id == submission_id).returning(SubmissionsModel.id)

    async with services['db_engine'].begin() as session:
       try:
           result = await session.execute(query)
           return result.first()
       except Exception as e:
           logger.error(e)
           raise e
       
async def get_sumbmission(submission_id: int):
    query  = select(SubmissionsModel).where(SubmissionsModel.id == submission_id)

    async with services['db_engine'].begin() as session:
        try:
            result  = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e

async def get_all_submissions():
    query  = select(SubmissionsModel)
    async with services['db_engine'].begin() as session:
        try:
            result  = await session.execute(query)
            return result.first()
        except Exception as e:
            logger.error(e)
            raise e
async def set_submission_status(submission: SubmissionUpdateDTO):
   query  = update(SubmissionsModel).where(submission.id).values(submission.to_dict()).returning(SubmissionsModel)

   async with services['db_engine'].begin() as session: 
       try:
           result  = await session.execute(query)
           return result.first()
       except Exception as e:
           logger.error(e)
           raise e





