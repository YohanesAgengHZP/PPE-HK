import os

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from api.dependencies import get_db
from api.models.attendance import AttendanceCreate, AttendanceResponse
from api.services.common import save_file
from api.services.attendance import get_all, create
from core.models import EmployeeAttendance


router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("", response_model=List[AttendanceResponse])
async def get_all_attendances(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("", response_model=AttendanceResponse)
async def create_attendance(
    new_attendance: AttendanceCreate,
    db: Session = Depends(get_db),
):
    attendance = EmployeeAttendance()
    attendance.employee_id = new_attendance.employee_id
    attendance.time = new_attendance.time
    attendance.work_status = new_attendance.work_status

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
