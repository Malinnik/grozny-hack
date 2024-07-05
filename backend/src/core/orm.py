import datetime
from sqlalchemy import ForeignKey, String, Date, Time, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
import uuid

from typing import Annotated

class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
uuidpk  = Annotated[uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now
)]

str_60 = Annotated[str, mapped_column(String(60))]
str_60_unique = Annotated[str, mapped_column(String(60), unique=True)]


class ImagesModel(Base):
    __tablename__  =  "images"
    id: Mapped[uuidpk]
    bucket: Mapped[str_60]
    path: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[created_at]

class DetectionsModel(Base):
    __tablename__  =  "detections"

    id: Mapped[intpk]
    name_folder: Mapped[str]
    name: Mapped[str]
    class_predict: Mapped[str]
    date_registration: Mapped[datetime.datetime]
    bbox: Mapped[str]
    registrations_id: Mapped[int]
    registration_class: Mapped[int]
    count: Mapped[int]
    max_count: Mapped[str]
    flag: Mapped[str]
    link: Mapped[str]


class RegistrationsModel(Base):
    __tablename__   =   "registrations"

    id: Mapped[intpk]
    name_folder: Mapped[str]
    detection_class: Mapped[str] = mapped_column(name="class")
    date_registration_start: Mapped[datetime.datetime]
    date_registration_end: Mapped[datetime.datetime]
    count: Mapped[int]