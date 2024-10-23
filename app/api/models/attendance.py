from datetime import datetime
from pydantic import BaseModel
from typing import List
from uuid import UUID

from api.models.common import Base64File


class AttendanceBase(BaseModel):
    employee_id: UUID
    time: datetime
    photo: str
    work_status: bool
    camera_name: str


class AttendanceResponse(AttendanceBase):
    name: str
    id: int


class AttendanceAllResponse(BaseModel):
    total_records: int
    filter_records: int
    results: List[AttendanceResponse]


class AttendanceCreate(AttendanceBase):
    photo: Base64File
