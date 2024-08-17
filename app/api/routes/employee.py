import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.dependencies import get_db
from api.models.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from api.services.common import delete_file, save_file
from api.services.employee import get_all, get_by_id, create, update, delete
from core.models import Employee


router = APIRouter(prefix="/employee", tags=["Employee"])


@router.get("", response_model=List[EmployeeResponse])
async def get_all_employee(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: UUID, db: Session = Depends(get_db)):
    return get_by_id(employee_id, db)


@router.post("", status_code=201, response_model=EmployeeResponse)
async def create_employee(new_employee: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee()
    employee.name = new_employee.name
    employee.company = new_employee.company
    employee.mcu = new_employee.mcu
    employee.photo = os.path.join("static", "ID", new_employee.photo.filename)

    await save_file(new_employee.photo.file_base64, new_employee.photo.filename, "ID")

    return create(employee, db)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: UUID,
    updated_employee: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    employee = Employee()
    employee.name = updated_employee.name
    employee.company = updated_employee.company
    employee.mcu = updated_employee.mcu

    if updated_employee.photo is not None:
        employee.photo = os.path.join("static", "ID", updated_employee.photo.filename)

        await save_file(
            updated_employee.photo.file_base64,
            updated_employee.photo.filename,
            "ID",
        )

    return update(employee_id, updated_employee, db)


@router.delete("/{employee_id}", status_code=204, response_model=None)
async def delete_employee(employee_id: UUID, db: Session = Depends(get_db)):

    # Get employee photo filename to be deleted
    employee = get_by_id(employee_id, db)
    filename = os.path.basename(employee.photo)

    delete(employee_id, db)

    await delete_file(filename, "ID")

    return None
