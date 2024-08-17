from pydantic import BaseModel
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


class EmployeeUpdate(EmployeeBase):
    pass
