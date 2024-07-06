import io
import aiohttp
from fastapi import APIRouter
from loguru import logger


from miniopy_async import Minio
from core.services import services
from common.db.pg_submissions import get_submission

submission = APIRouter()

@submission.get("/v1/submissions", tags=["Download"])
async def download_submission(id: int):
    s3: Minio = services['s3_client']
    
    try:
        submission = await get_submission(id)
    except Exception as e:
        logger.error(e)
        return {"error": "Submission not found"}

    

    obj = await s3.list_objects("submissions")
    try:
        async with aiohttp.ClientSession() as session:
            response = await s3.get_object("submissions", obj[id]._object_name, session)
            logger.debug(f"{response=}")
            body = io.BytesIO(await response.read())
            logger.debug(f"{body=}")
    except Exception as e:
        logger.exception(e)