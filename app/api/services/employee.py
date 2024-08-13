import aiofiles
import binascii
import os

from base64 import b64decode
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Union
from uuid import UUID

from core.models import Employee
from core.settings import STATIC_ROOT


def get_all(db: Session) -> List[Employee]:
    """Get all employees."""

    return db.query(Employee).all()


def get_by_id(employee_id: UUID, db: Session) -> Employee:
    """Get an employee by ID."""

    employee: Union[Employee, None] = db.query(Employee).get(employee_id)

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

    current_employee = get_by_id(employee_id, db)

    return current_employee


def delete(employee_id: UUID, db: Session) -> None:
    """Delete an employee."""

    employee = get_by_id(employee_id, db)

    db.delete(employee)
    db.commit()


async def save_photo(photo_base64: str, filename: str):
    """Decode base64 photo and save to static folder"""

    try:
        photo_content = b64decode(photo_base64.encode("utf-8"))
        folder_path = os.path.join(STATIC_ROOT, "ID")
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        filepath = os.path.join(folder_path, filename)
        async with aiofiles.open(filepath, "wb") as out_file:
            await out_file.write(photo_content)
    except binascii.Error:
        raise HTTPException(
            status_code=400,
            detail="There was an error decoding the base64 string",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="There was an error uploading the file(s)",
        )
