from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.dependencies import get_db
from app.api.models.employee import EmployeeCreate, EmployeeUpdate
from app.api.services.employee import get_all, get_by_id, create, update, delete


router = APIRouter(prefix="/employee", tags=["Employee"])


@router.get("")
async def get_all_employee(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{employee_id}")
async def get_employee(employee_id: UUID, db: Session = Depends(get_db)):
    return get_by_id(employee_id, db)


@router.post("", status_code=201)
async def create_employee(new_employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create(new_employee, db)


@router.put("/{employee_id}")
async def update_employee(
    employee_id: UUID, updated_employee: EmployeeUpdate, db: Session = Depends(get_db)
):
    return update(employee_id, updated_employee, db)


@router.delete("/{employee_id}", status_code=204)
async def delete_employee(employee_id: UUID, db: Session = Depends(get_db)):
    return delete(employee_id, db)
