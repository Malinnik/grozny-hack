import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from miniopy_async import Minio

from core.orm import Base


services = {}

async def __create_db_engine() -> AsyncEngine:
    return create_async_engine(
        os.getenv("POSTGRES_URL"),
        pool_size=4,
        max_overflow=8,
        pool_recycle=120,
        pool_pre_ping=True,
        future=True,
    )

async def __create_db_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as session:
        # FIX: coment line below before deploying server
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)


async def __create_s3_client() -> Minio:
    return Minio(
        endpoint=os.getenv("S3_ENDPOINT"),
        access_key=os.getenv("S3_ACCESS_KEY"),
        secret_key=os.getenv("S3_SECRET_KEY"),
        region=os.getenv("S3_REGION", 'ru_1'),
        secure=os.getenv("S3_SECURE", False),
    )
async def __init_bucket(s3: Minio):
    if not await s3.bucket_exists("data"):
        await s3.make_bucket("data", os.getenv("S3_REGION", 'ru_1'))


@asynccontextmanager
async def lifespan(app: FastAPI):

    # On startup
    engine = await __create_db_engine()
    services['db_engine'] = engine
    await __create_db_tables(engine)

    s3_client  = await __create_s3_client()
    services['s3_client'] = s3_client
    await __init_bucket(s3_client)

    yield
    # On shutdown 