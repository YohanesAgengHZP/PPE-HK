from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from api.dependencies import get_db
from api.models.report import ReportCreate, ReportResponse, ReportUpdate
from api.services.report import get_all, get_by_id, create, update
from core.models import Report


router = APIRouter(prefix="/report", tags=["Report"])


@router.get("", response_model=List[ReportResponse])
async def get_all_report(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, db: Session = Depends(get_db)):
    return get_by_id(report_id, db)


@router.post("", status_code=201, response_model=ReportResponse)
async def create_report(new_report: ReportCreate, db: Session = Depends(get_db)):
    report = Report()
    report.reason = new_report.reason
    report.image_url = new_report.image_url
    report.camera_name = new_report.camera_name
    report.num_of_people = new_report.num_of_people
    report.people_without_ppe_id = new_report.people_without_ppe_id

    return create(report, db)


@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int, updated_report: ReportUpdate, db: Session = Depends(get_db)
):
    report = Report()
    report.notes = updated_report.notes
    report.person_responsible = updated_report.person_responsible
    report.is_closed = updated_report.is_closed

    return update(report_id, report, db)