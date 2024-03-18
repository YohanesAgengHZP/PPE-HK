from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class AttendanceBase(BaseModel):
    employee_id: UUID
    time: datetime
    photo: str
    work_status: bool


class AttendanceResponse(AttendanceBase):
    id: int


# TODO: Remove after testing
class AttendanceCreate(AttendanceBase):
    pass
