from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from api.dependencies import get_db
from api.models.attendance import AttendanceCreate, AttendanceResponse
from api.services.attendance import get_all
from core.models import EmployeeAttendance


router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("", response_model=List[AttendanceResponse])
async def get_all_attendances(db: Session = Depends(get_db)):
    return get_all(db)


# TODO: Remove after testing
@router.post("", response_model=AttendanceResponse)
async def create_attendance(
    new_attendance: AttendanceCreate, db: Session = Depends(get_db)
):
    attendance = EmployeeAttendance()
    attendance.employee_id = new_attendance.employee_id
    attendance.time = new_attendance.time
    attendance.photo = new_attendance.photo
    attendance.work_status = new_attendance.work_status

    db.add(attendance)
    db.commit()

    return attendance
