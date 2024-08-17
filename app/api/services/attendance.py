from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from api.services.employee import get_by_id
from core.models import Employee, EmployeeAttendance


def get_all(db: Session) -> List[EmployeeAttendance]:
    """Get all employees attendance."""

    statement = select(
        EmployeeAttendance.id,
        EmployeeAttendance.employee_id,
        EmployeeAttendance.time,
        EmployeeAttendance.photo,
        EmployeeAttendance.work_status,
        Employee.name,
    ).join(Employee)
    result = db.execute(statement)

    return [attendance._asdict() for attendance in result.all()]


def create(attendance: EmployeeAttendance, db: Session) -> EmployeeAttendance:
    """Create a new attendance."""

    # Check if employee is valid
    _ = get_by_id(attendance.employee_id, db)

    db.add(attendance)
    db.commit()

    return attendance
