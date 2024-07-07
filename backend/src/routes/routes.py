import io
import zipfile
import PIL.Image
import aiohttp
import uuid
import pandas as pd
from fastapi import APIRouter, File, Response, UploadFile, Form

from datetime import datetime
from fastapi.responses import StreamingResponse
from loguru import logger
from miniopy_async import Minio

from annotations.objects import ImageAddDTO, ImagesIds, Submission, SubmissionAddDTO, SubmissionUpdateDTO
from common.db.pg_submissions import add_submission, set_submission_status
from common.registrations import generate_registrations, get_exif_date, set_predictions
from common.neuro import predict_image, predict_with_clip
from common.db.pg_image import add_image_to_db, get_image_path, get_images_ids, get_max_pages
from core.services import services, models
from core.orm import SubmissionStatus


router = APIRouter()

@router.post("/v1/archive/upload", tags=["Upload"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(True), shof_conf: bool = Form(True)):
    try:
        contents = await file.read()
        
        submission_name = f"submission-{datetime.now()}.csv"
        res = await add_submission(SubmissionAddDTO(path=submission_name))
        subm = Submission.model_validate(res)

        list_all_predictions = []
        # read zip from contents
        with zipfile.ZipFile(io.BytesIO(contents)) as zip:
            for file in zip.namelist():
                # prefix = True
                if "/" not in file:
                    continue
                    # prefix = False
                logger.debug(f"{file=}")
                # 1/name.jpg
                with zip.open(file) as f:
                    contents = f.read()
                    try:
                        with PIL.Image.open(io.BytesIO(contents)) as img:
                            exif = get_exif_date(img, file)
                            
                            [img, list_predictions] = await predict_image(img, file,  models['classifier'], models['detector'],use_label=use_label, show_conf=shof_conf)

                            list_predictions = [i + [exif] for i in list_predictions]
                            logger.debug(f"{list_predictions=}")

                            list_all_predictions.extend(list_predictions)
                            
                            contents = io.BytesIO()
                            img.save(contents, format="PNG")
                            contents.seek(0)

                            s3:Minio = services['s3_client']
                            id: uuid.UUID = uuid.uuid4()

                            _ = file.split("/")[0]
                            filename: str = f"{_}/{id}.png"

                            await add_image_to_db(ImageAddDTO(id=id, bucket="data", path=filename))
                            await s3.put_object("data", filename, contents, contents.getbuffer().nbytes)
                            contents.seek(0)

                            contents = contents.read()
                            
                    
                    except Exception as e:
                        await set_submission_status(SubmissionUpdateDTO(id=subm.id, status=SubmissionStatus.Exited))
                        logger.exception(e)
                        return Response(status_code=500)


        predictions = set_predictions(list_all_predictions)
        
        registrations = generate_registrations(predictions)

        # file
        df = pd.DataFrame(registrations)
        df.to_csv('submission.csv', index=False)


        # bytes
        contents = io.BytesIO()
        df.to_csv(contents, index=False)
        contents.seek(0)


        await s3.put_object("submissions", submission_name, contents, contents.getbuffer().nbytes)
        await set_submission_status(SubmissionUpdateDTO(id=subm.id, status=SubmissionStatus.Ready))
        contents.seek(0)
        contents = contents.read()
        
        return Response(contents, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=submission.csv"})


    except Exception as e:
        await set_submission_status(SubmissionUpdateDTO(id=subm.id, status=SubmissionStatus.Exited))
        logger.exception(e)
        return Response(status_code=500)

@router.post("/v1/archive/upload/clip", tags=["Test"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(False), shof_conf: bool = Form(False)):
    try:
        contents = await file.read()

        submission_name = f"submission-{datetime.now()}.csv"
        res = await add_submission(SubmissionAddDTO(path=submission_name))
        subm = Submission.model_validate(res)


        list_all_predictions = []
        # read zip from contents
        with zipfile.ZipFile(io.BytesIO(contents)) as zip:
            for file in zip.namelist():
                if "/" not in file:
                    continue
                logger.debug(f"{file=}")
                # 1/name.jpg
                with zip.open(file) as f:
                    contents = f.read()
                    try:
                        with PIL.Image.open(io.BytesIO(contents)) as img:
                            exif = get_exif_date(img, file)
                            
                            [img, list_predictions] = await predict_with_clip(img, file, models['clip'], models['preprocessor'], models['detector'] ,use_label=use_label, show_conf=shof_conf)

                            list_predictions = [i + [exif] for i in list_predictions]
                            logger.debug(f"{list_predictions=}")

                            list_all_predictions.extend(list_predictions)
                            
                            contents = io.BytesIO()
                            img.save(contents, format="PNG")
                            contents.seek(0)

                            s3:Minio = services['s3_client']
                            id: uuid.UUID = uuid.uuid4()

                            _ = file.split("/")[0]
                            filename: str = f"{_}/{id}.png"

                            await add_image_to_db(ImageAddDTO(id=id, bucket="data", path=filename))
                            await s3.put_object("data", filename, contents, contents.getbuffer().nbytes)
                            contents.seek(0)

                            contents = contents.read()
                            
                    
                    except Exception as e:
                        await set_submission_status(SubmissionUpdateDTO(id=subm.id, status=SubmissionStatus.Exited))
                        logger.exception(e)
                        return Response(status_code=500)


        predictions = set_predictions(list_all_predictions)
        
        registrations = generate_registrations(predictions)

        # file
        df = pd.DataFrame(registrations)
        df.to_csv('submission.csv', index=False)

        # bytes
        contents = io.BytesIO()
        df.to_csv(contents, index=False)
        contents.seek(0)

        await s3.put_object("submissions", submission_name, contents, contents.getbuffer().nbytes)
        await set_submission_status(SubmissionUpdateDTO(id=subm.id, status=SubmissionStatus.Ready))
        contents.seek(0)
        contents = contents.read()
        
        return Response(contents, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=submission.csv"})


    except Exception as e:
        await set_submission_status(SubmissionUpdateDTO(id=subm.id, status=SubmissionStatus.Exited))
        logger.exception(e)
        return Response(status_code=500)



@router.post("/v1/image/upload", tags=["Upload"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(False), shof_conf: bool = Form(False)):
    try:
        contents = await file.read()
        
        with PIL.Image.open(io.BytesIO(contents)) as img:
            [img, list_predictions] = await predict_image(img, models['classifier'], models['detector'], use_label=use_label, show_conf=shof_conf)

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

@router.get("/v1/test/download", tags=["Download"])
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

@router.get("/v2/images/download", tags=["Images"])
async def get_file_by_id(id: uuid.UUID):
    s3: Minio = services['s3_client']
    
    _ = await get_image_path(id)
    logger.debug(f"{id=}")
    if not _:
        return Response(status_code=404)
    [bucket, path] = _ 
    logger.debug(f"file: {bucket}/{path}")

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

@router.get("/v1/images", tags=["Images"])
async def get_images(page: int):
    try:
        result = await get_images_ids(page)
        ids = [ImagesIds.model_validate(i) for i in result]
        return ids
    except Exception as e:
        logger.error(e)

@router.get("/v1/images/pages", tags=["Images"])
async def get_pages_amount():
    try:
        result = await get_max_pages()
        return result
    except Exception as e:
        logger.error(e)


@router.get("/v1/test/zip", tags=["Download"])
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


    
    
