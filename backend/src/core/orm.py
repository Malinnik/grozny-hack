import datetime
import enum
from sqlalchemy import Enum, ForeignKey, String, Date, Time, text
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


class SubmissionStatus(enum.Enum):
    Procces = "process"
    Exited = "exited"
    Ready = "ready"


class ImagesModel(Base):
    __tablename__  =  "images"
    id: Mapped[uuidpk]
    bucket: Mapped[str_60]
    path: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[created_at]
    
class SubmissionsModel(Base):
    __tablename__ = "submissions"
    id: Mapped[intpk]
    bucket: Mapped[str_60] = mapped_column(default="submissions")
    path: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[created_at]
    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus), server_default=SubmissionStatus.Procces.name)

class RegistrationsModel(Base):
    __tablename__ = "registrations"

    id: Mapped[intpk]
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"))
    name_folder: Mapped[str]
    detection_class: Mapped[str] = mapped_column(name="class")
    date_registration_start: Mapped[datetime.datetime]
    date_registration_end: Mapped[datetime.datetime]
    count: Mapped[int]