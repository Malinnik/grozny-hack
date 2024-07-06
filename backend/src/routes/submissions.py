import io
import aiohttp
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from loguru import logger
from datetime import datetime

from miniopy_async import Minio
from annotations.objects import Submission
from core.services import services
from common.db.pg_submissions import get_all_submissions, get_submission

submission = APIRouter()

@submission.get("/v1/submissions/csv", tags=["Submissions"])
async def download_submission(id: int):
    s3: Minio = services['s3_client']
    
    try:
        result = await get_submission(id)
        submission = Submission.model_validate(result)
    except Exception as e:
        logger.error(e)
        return Response(status_code=404)

    

    try:
        async with aiohttp.ClientSession() as session:
            logger.debug(await s3.list_objects("submissions"))
            logger.debug(submission.path)
            if submission.path not in [obj._object_name for obj in await s3.list_objects("submissions")]:
                return Response(status_code=404)
            response = await s3.get_object("submissions", submission.path, session)
            content = io.BytesIO(await response.read())
        
        return StreamingResponse(content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={submission.path}"})
    except Exception as e:  
        logger.exception(e)
        return Response(status_code=500)
    
@submission.get("/v1/submissions", tags=["Submissions"])
async def sumbissions_list():
    try:
        result = await get_all_submissions()
        submissions = [Submission.model_validate(i).to_response() for i in result] 
        
        return submissions
    except Exception as e:
        logger.error(e)
        return Response(status_code=404)