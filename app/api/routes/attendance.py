import os

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Union

from api.dependencies import get_db
from api.models.attendance import (
    AttendanceAllResponse,
    AttendanceCreate,
    AttendanceResponse,
)
from api.services.common import count_all, save_file
from api.services.attendance import get_all, create
from core.models import EmployeeAttendance


router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get(
    "",
    description="Get all employees attendance. Filter are optional. Can filter based on list of camera tags.",
    response_model=AttendanceAllResponse,
)
async def get_all_attendances(
    tags: Union[str, None] = None,
    start: Union[datetime, None] = None,
    end: Union[datetime, None] = None,
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db),
):
    tag_array = [tag.strip() for tag in tags.split(",")] if tags else None
    count, results = get_all(tag_array, start, end, limit, page, db)

    return {
        "total_records": count_all(EmployeeAttendance.id, db),
        "filter_records": count,
        "results": results,
    }


@router.post("", response_model=AttendanceResponse)
async def create_attendance(
    new_attendance: AttendanceCreate,
    db: Session = Depends(get_db),
):
    attendance = EmployeeAttendance()
    attendance.employee_id = new_attendance.employee_id
    attendance.time = new_attendance.time
    attendance.work_status = new_attendance.work_status
    attendance.camera_name = new_attendance.camera_name

    current_date = str(datetime.now().date())
    photo_url = os.path.join(
        "static",
        "attendance",
        current_date,
        new_attendance.photo.filename,
    )
    attendance.photo = photo_url

    await save_file(
        new_attendance.photo.file_base64,
        new_attendance.photo.filename,
        os.path.join("attendance", current_date),
    )

    return create(attendance, db)
