from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Tuple, Union

from api.services.employee import get_by_id
from core.models import Camera, Employee, EmployeeAttendance


def get_all(
    tags: Union[List[str], None],
    start: Union[datetime, None],
    end: Union[datetime, None],
    limit: int,
    page: int,
    db: Session,
) -> Tuple[int, List[EmployeeAttendance]]:
    """
    Get all employees attendance. Filter are optional.

    Can filter based on list of camera tags.

    Returns:
        results (Tuple[int, List[EmployeeAttendance]]): Tuple of total number of records and the results per page.
    """

    count_query = (
        db.query(func.count(EmployeeAttendance.id))
        .join(Employee)
        .join(Camera, EmployeeAttendance.camera_name == Camera.name)
    )
    query = (
        db.query(
            EmployeeAttendance.id,
            EmployeeAttendance.employee_id,
            EmployeeAttendance.time,
            EmployeeAttendance.photo,
            EmployeeAttendance.work_status,
            EmployeeAttendance.camera_name,
            Employee.name,
        )
        .join(Employee)
        .join(Camera, EmployeeAttendance.camera_name == Camera.name)
    )

    if tags:
        count_query = count_query.filter(Camera.tags.overlap(tags))
        query = query.filter(Camera.tags.overlap(tags))

    if start is not None:
        count_query = count_query.filter(EmployeeAttendance.time >= start)
        query = query.filter(EmployeeAttendance.time >= start)

    if end is not None:
        count_query = count_query.filter(EmployeeAttendance.time <= end)
        query = query.filter(EmployeeAttendance.time <= end)

    if limit <= 0:
        limit = 10

    if page <= 0:
        page = 1

    count = count_query.scalar()
    results = (
        query.order_by(EmployeeAttendance.time.desc())
        .limit(limit)
        .offset((page - 1) * limit)
        .all()
    )

    return count, results


def create(attendance: EmployeeAttendance, db: Session) -> EmployeeAttendance:
    """Create a new attendance."""

    # Check if employee is valid
    _ = get_by_id(attendance.employee_id, db)

    db.add(attendance)
    db.commit()

    return attendance
