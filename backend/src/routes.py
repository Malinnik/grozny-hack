import io
import zipfile
import PIL.Image
import aiohttp
import uuid
import pandas as pd
from fastapi import APIRouter, File, Response, UploadFile, Form

from datetime import datetime, timedelta
from fastapi.responses import StreamingResponse
from loguru import logger
from miniopy_async import Minio

from annotations.objects import ImageAddDTO
from common.neuro import predict_image, predict_with_clip
from common.db.pg_image import add_image_to_db, get_image_path
from core.services import services, models


router = APIRouter()


def most_common(lst):
    return max(set(lst), key=lst.count)

def get_exif_date(img, file):
    exif = img._getexif()
    if not exif:
        logger.error(f'Image {file} does not have EXIF data.')
    return datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')


def generate_registrations(predictions):
    # name_folder,class,date_registration_start,date_registration_end,count
    registrations = []
    
    predictions['name_folder'] = predictions['link'].apply(lambda x: x[:x.find('/')])
    for name_folder, group in predictions.groupby('name_folder'):
        dates = []
        classes = []
        counts = []
        for shortpath, obj in group.groupby('link'):
            
            counts.append(min(len(obj), 5))
            dates.append(obj['exif'].iloc[0])

            cls = []
            for id, obj in obj.iterrows():
                cls.append(obj['class_name_predicted'])
            classes.append(cls)
        # print(dates[:5])
        # print(counts[:5])
        # print(classes[:5])

        prev_date = dates[0]
        prev_class = most_common(classes[0])
        prev_count = counts[0]
        registrations.append({
            'name_folder': name_folder, 
            'class': prev_class,
            'classdate_registration_start': prev_date, 
            'date_registration_end': prev_date, 
            'count': prev_count,
        })
        for i, (date, cls, count) in enumerate(zip(dates[1:], classes[1:], counts[1:])):
            cls = most_common(cls)

            if cls == prev_class and count == prev_count and (date - prev_date).seconds//3600 < 30:
                registrations[-1]['date_registration_end'] = date
            else:
                registrations.append({
                    'name_folder': name_folder, 
                    'class': cls,
                    'classdate_registration_start': date, 
                    'date_registration_end': date, 
                    'count': count,
                })
            
            prev_date = date
            prev_class = cls
            prev_count = count
        registrations[-1]['date_registration_end'] = date
        
    return registrations


@router.post("/v1/archive/upload", tags=["Test"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(False), shof_conf: bool = Form(False)):
    try:
        contents = await file.read()
        
        list_all_predictions = []
        # read zip from contents
        with zipfile.ZipFile(io.BytesIO(contents)) as zip:
            for file in zip.namelist():
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

                            filename: str = f"{id}.png"

                            await add_image_to_db(ImageAddDTO(id=id, bucket="data", path=filename))
                            await s3.put_object("data", filename, contents, contents.getbuffer().nbytes)
                            contents.seek(0)

                            contents = contents.read()
                            
                    
                    except Exception as e:
                        logger.exception(e)
                        return Response(status_code=500)


        predictions = pd.DataFrame(list_all_predictions, columns=["link", "class_name_predicted", "confidence", "exif"])
        
        registrations = generate_registrations(predictions)

        # file
        df = pd.DataFrame(registrations)
        df.to_csv('submission.csv', index=False)
        print('Saved to submission.csv')


        # bytes
        contents = io.BytesIO()
        df.to_csv(contents, index=False)
        contents.seek(0)
        contents = contents.read()
        
        return Response(contents, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=submission.csv"})


    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)

@router.post("/v1/archive/upload/clip", tags=["Test"])
async def create_upload_file(file: UploadFile = File(...), use_label: bool = Form(False), shof_conf: bool = Form(False)):
    try:
        contents = await file.read()
        
        list_all_predictions = []
        # read zip from contents
        with zipfile.ZipFile(io.BytesIO(contents)) as zip:
            for file in zip.namelist():
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

                            filename: str = f"{id}.png"

                            await add_image_to_db(ImageAddDTO(id=id, bucket="data", path=filename))
                            await s3.put_object("data", filename, contents, contents.getbuffer().nbytes)
                            contents.seek(0)

                            contents = contents.read()
                            
                    
                    except Exception as e:
                        logger.exception(e)
                        return Response(status_code=500)


        predictions = pd.DataFrame(list_all_predictions, columns=["link", "class_name_predicted", "confidence", "exif"])
        
        registrations = generate_registrations(predictions)

        # file
        df = pd.DataFrame(registrations)
        df.to_csv('submission.csv', index=False)
        print('Saved to submission.csv')


        # bytes
        contents = io.BytesIO()
        df.to_csv(contents, index=False)
        contents.seek(0)
        contents = contents.read()
        
        return Response(contents, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=submission.csv"})


    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)



@router.post("/v1/image/upload", tags=["Test"])
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
    