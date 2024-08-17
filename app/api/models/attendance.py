from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from api.models.common import Base64File


class AttendanceBase(BaseModel):
    employee_id: UUID
    time: datetime
    photo: str
    work_status: bool


class AttendanceResponse(AttendanceBase):
    name: str
    id: int


class AttendanceCreate(AttendanceBase):
    photo: Base64File
