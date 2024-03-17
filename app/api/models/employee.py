from pydantic import BaseModel
from uuid import UUID


class EmployeeBase(BaseModel):
    id: UUID


class EmployeeCreate(EmployeeBase):
    name: str
    company: str
    mcu: bool
    photo: str


class EmployeeUpdate(EmployeeBase):
    pass
