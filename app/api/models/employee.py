from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from api.models.common import Base64File


class EmployeeBase(BaseModel):
    name: str
    company: str
    mcu: bool
    photo: str


class EmployeeResponse(EmployeeBase):
    id: UUID


class EmployeeCreate(EmployeeBase):
    photo: Base64File


class EmployeeUpdate(BaseModel):
    name: Optional[str]
    company: Optional[str]
    mcu: Optional[bool]
    photo: Optional[Base64File]
