from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

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
