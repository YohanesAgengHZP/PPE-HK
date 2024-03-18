from sqlalchemy.orm import Session
from typing import List

from core.models import EmployeeAttendance


def get_all(db: Session) -> List[EmployeeAttendance]:
    """Get all employees attendance."""
    return db.query(EmployeeAttendance).all()
