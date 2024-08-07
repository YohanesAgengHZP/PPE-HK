import os

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Literal, Union

from api.dependencies import get_db
from api.models.report import ReportCreate, ReportResponse, ReportUpdate
from api.services.report import (
    get_all,
    get_by_id,
    get_chart,
    create,
    save_image,
    update,
)
from core.models import Report


router = APIRouter(prefix="/report", tags=["Report"])


@router.get(
    "",
    description="Get all reports. Type are prioritized over reasons.",
    response_model=List[ReportResponse],
)
async def get_all_report(
    type: Union[Literal["ppe", "animal", "danger"] | None] = None,
    reasons: Union[str, None] = None,
    start: Union[datetime, None] = None,
    end: Union[datetime, None] = None,
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db),
):
    reason_array = reasons.split(",") if reasons else None
    return get_all(type, reason_array, start, end, limit, page, db)


# TODO: Add response_model
@router.get("/chart")
async def get_report_chart(
    start: Union[datetime, None] = None,
    end: Union[datetime, None] = None,
    db: Session = Depends(get_db),
):
    return get_chart(start, end, db)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, db: Session = Depends(get_db)):
    return get_by_id(report_id, db)


@router.post("", status_code=201, response_model=ReportResponse)
async def create_report(new_report: ReportCreate, db: Session = Depends(get_db)):
    report = Report()
    report.timestamp = new_report.timestamp
    report.reason = new_report.reason
    report.camera_name = new_report.camera_name
    report.num_of_people = new_report.num_of_people
    report.people_without_ppe_id = new_report.people_without_ppe_id

    current_date = str(datetime.now().date())
    image_url = os.path.join("static", current_date, new_report.image.filename)
    report.image_url = image_url

    save_image(new_report.image.file_base64, new_report.image.filename, current_date)

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
