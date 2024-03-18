from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class AttendanceBase(BaseModel):
    employee_id: UUID
    start: datetime
    end: datetime
    start_photo: str
    end_photo: str


class AttendanceResponse(AttendanceBase):
    id: int


# TODO: Remove after testing
class AttendanceCreate(AttendanceBase):
    pass
