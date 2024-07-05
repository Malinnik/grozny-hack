from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, UUID4


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


class Ok(BaseModel):
    ok: str = "Ok"

    
class Error(BaseModel):
    error: str = Field(description="Error message")