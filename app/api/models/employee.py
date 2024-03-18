from pydantic import BaseModel
from uuid import UUID


class EmployeeBase(BaseModel):
    name: str
    company: str
    mcu: bool
    photo: str


class EmployeeResponse(EmployeeBase):
    id: UUID


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass
