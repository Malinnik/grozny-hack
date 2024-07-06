from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, Field, UUID4

from core.orm import SubmissionStatus


class ImageAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    bucket: str = Field(max_length=60, default="data")
    path: str

    def to_dict(self):
        return {
            "id": self.id,
            "bucket": self.bucket,
            "path": self.path,
    }

class Image(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    bucket: str = Field(max_length=60)
    path: str
    created_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "bucket": self.bucket,
            "path": self.path,
            "date": str(self.date),
    }


class SubmissionAddDTO(BaseModel):
    model_config  = ConfigDict(from_attributes=True)

    path: str

    def to_dict(self):
        return {
            "path": self.path,
    }

class SubmissionUpdateDTO(BaseModel):
    model_config  = ConfigDict(from_attributes=True)

    id: int
    status: SubmissionStatus

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
    }

class Submission(BaseModel):
    model_config  = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    bucket: str = Field(max_length=60, default="submissions")
    path: str

    created_at: datetime
    status: SubmissionStatus

    def to_dict(self):
        return {
            "id": self.id,
            "bucket": self.bucket,
            "path": self.path,
            "created_at": str(self.created_at),
            "status": self.status,
    }

    def to_response(self):
        return {
            "id": self.id,
            "bucket": self.bucket,
            "path": self.path,
            "created_at": str(self.created_at.strftime("%d-%m-%Y %H:%M:%S")),
            "status": self.status,
    }



class RegistrationAddDTO(BaseModel):
    name_folder: str
    detection_class: str
    date_registration_start: datetime
    date_registration_end: datetime
    count: int

    def to_dict(self):
        return {
            "name_folder": self.name_folder,
            "detection_class": self.detection_class,
            "date_registration_start": str(self.date_registration_start),
            "date_registration_end": str(self.date_registration_end),
            "count": self.count,
    }



class Ok(BaseModel):
    ok: str = "Ok"

    
class Error(BaseModel):
    error: str = Field(description="Error message")