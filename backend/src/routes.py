import io
import zipfile
import PIL.Image
import aiohttp
import uuid
from fastapi import APIRouter, File, Response, UploadFile, Form

from fastapi.responses import StreamingResponse
from loguru import logger
from miniopy_async import Minio

from annotations.objects import ImageAddDTO
from common.neuro import predict_image
from common.db.pg_image import add_image_to_db, get_image_path
from core.services import services, models


router = APIRouter()

@router.post("/v1/archive/upload", tags=["Test"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(False), shof_conf: bool = Form(False)):
    try:
        contents = await file.read()
        
        # read zip from contents

        # read files from zip file



        # logger.debug(f"{use_label=}      {shof_conf=}")

        # s3:Minio = services['s3_client']
        
        # id: uuid.UUID = uuid.uuid4()
        
        # # Set Filename
        # _ = file.filename.split(".")
        # _[0] = str(id) + '.'
        # filename: str = "".join(_)
        
        # logger.debug(f"{filename=}")

        # await add_image_to_db(ImageAddDTO(id=id, bucket="data", path=filename))
        # await s3.put_object("data", filename, io.BytesIO(contents), len(contents))
        
        return Response(contents, media_type="image/*")
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)





@router.post("/v1/image/upload", tags=["Test"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(False), shof_conf: bool = Form(False)):
    try:
        contents = await file.read()
        
        with PIL.Image.open(io.BytesIO(contents)) as img:
            img = await predict_image(img, models['classifier'], models['detector'], use_label=use_label, show_conf=shof_conf)

            contents = io.BytesIO()
            img.save(contents, format="PNG")
            contents.seek(0)

            s3:Minio = services['s3_client']
            id: uuid.UUID = uuid.uuid4()

            filename: str = f"{id}.png"
            logger.debug(f"{filename=}")

            await add_image_to_db(ImageAddDTO(id=id, bucket="data", path=filename))
            await s3.put_object("data", filename, contents, contents.getbuffer().nbytes)
            contents.seek(0)

            contents = contents.read()
            
        return Response(contents, media_type="image/*")
    
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)

@router.get("/v1/test/download", tags=["Test"])
async def get_file_test():
    s3: Minio = services['s3_client']
    

    obj = await s3.list_objects("data")
    try:
        async with aiohttp.ClientSession() as session:
            response = await s3.get_object("data", obj[0]._object_name, session)
            logger.debug(f"{response=}")
            body = io.BytesIO(await response.read())
            logger.debug(f"{body=}")
    except Exception as e:
        logger.exception(e)
    # finally:
    #     response.close() 
    #     response.release()
        
    return StreamingResponse(body, media_type="image/*")

@router.get("/v2/test/download", tags=["Test"])
async def get_file_by_id(id: uuid.UUID):
    s3: Minio = services['s3_client']
    
    _ = await get_image_path(id)
    logger.debug(f"{id=}")
    if not _:
        return Response(status_code=404)
    [bucket, path] = _ 
    logger.debug(f"file: {bucket}/{path}")

    obj = await s3.list_objects("data")
    try:
        async with aiohttp.ClientSession() as session:
            response = await s3.get_object(bucket, path, session)
            logger.debug(f"{response=}")
            body = io.BytesIO(await response.read())
            logger.debug(f"{body=}")
    except Exception as e:
        logger.exception(e)
    # finally:
    #     response.close() 
    #     response.release()
        
    return StreamingResponse(body, media_type="image/*")


@router.get("/v1/test/zip", tags=["Test"])
async def get_files():
    s3: Minio = services['s3_client']
    
    objects = await s3.list_objects("data")

    with zipfile.ZipFile("images.zip", "w") as zip_file:
        for obj in objects:
            try:
                async with aiohttp.ClientSession() as session:
                    response = await s3.get_object("data", obj._object_name, session)
            
                    body = await response.read()
                    
                await zip_file.writestr(obj._object_name, body)

            except Exception as e:
                logger.exception(e)
        

    with open("images.zip", "rb") as file:
        zip_data = file.read()
    
    return Response(zip_data, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=images.zip"})
    