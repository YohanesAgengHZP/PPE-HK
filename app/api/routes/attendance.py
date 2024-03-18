from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.services.attendance import get_all


router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("")
async def get_all_attendances(db: Session = Depends(get_db)):
    return get_all(db)
