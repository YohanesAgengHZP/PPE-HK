from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from core.models import Employee, EmployeeAttendance


def get_all(db: Session) -> List[EmployeeAttendance]:
    """Get all employees attendance."""
    statement = select(Employee.name, EmployeeAttendance).join(EmployeeAttendance)
    return db.execute(statement)
