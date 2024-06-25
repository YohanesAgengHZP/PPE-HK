from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class CameraBase(BaseModel):
    name: str
    url: str
    active: bool
    tags: Optional[list[str]]


class CameraResponse(CameraBase):
    id: UUID


class CameraActiveStatus(BaseModel):
    active: bool


class CameraCreate(CameraBase):
    pass


class CameraUpdate(CameraBase):
    pass
