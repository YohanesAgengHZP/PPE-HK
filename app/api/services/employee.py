from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from core.models import Employee


def get_all(db: Session) -> List[Employee]:
    """Get all employees."""
    return db.query(Employee).all()


def get_by_id(employee_id: UUID, db: Session) -> Employee:
    """Get an employee by ID."""
    employee: Employee = db.query(Employee).get(employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found",
        )

    return employee


def create(employee: Employee, db: Session) -> UUID:
    """Create a new employee."""
    db.add(employee)
    db.commit()

    return employee


# TODO: Implement the update function
def update(employee_id: UUID, updated_employee: Employee, db: Session) -> Employee:
    """Update an employee."""
    current_employee = db.query(Employee).get(employee_id)

    if not current_employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found",
        )

    return updated_employee


def delete(employee_id: UUID, db: Session) -> None:
    """Delete an employee."""
    employee = db.query(Employee).get(employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found",
        )

    db.delete(employee)
    db.commit()
