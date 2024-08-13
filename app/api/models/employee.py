from pydantic import BaseModel
from uuid import UUID

from api.models.common import Base64File


class EmployeeBase(BaseModel):
    name: str
    company: str
    mcu: bool
    photo_url: str


class EmployeeResponse(EmployeeBase):
    id: UUID


class EmployeeCreate(BaseModel):
    name: str
    company: str
    mcu: bool
    photo: Base64File


class EmployeeUpdate(EmployeeBase):
    pass
