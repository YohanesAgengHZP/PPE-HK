import aiofiles
import binascii
import os

from base64 import b64decode
from datetime import datetime
from fastapi import HTTPException
from re import sub
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Literal, Union
from uuid import UUID

from core.models import Report
from core.settings import STATIC_ROOT


PPE_CLASS_NAME_LIST = ["NO-Hardhat", "NO-Safety Shoes", "NO-Safety Vest"]
DANGER_CLASS_NAME_LIST = ["Fire", "Puddle", "Smoke", "Smoking"]


def get_all(
    type: Union[Literal["ppe", "animal", "danger"] | None],
    reasons: Union[List[str], None],
    start: Union[datetime, None],
    end: Union[datetime, None],
    limit: int,
    page: int,
    db: Session,
) -> List[Report]:
    """Get all reports. Filter are optional. Type are prioritized over reasons."""

    query = db.query(Report)

    if type:
        match type:
            # case "animal":
            #     query = query.filter(Report.reason.overlap([""]))
            case "danger":
                query = query.filter(Report.reason.overlap(DANGER_CLASS_NAME_LIST))
            case "ppe":
                query = query.filter(Report.reason.overlap(PPE_CLASS_NAME_LIST))
    elif reasons:
        query = query.filter(Report.reason.overlap(reasons))

    if start is not None:
        query = query.filter(Report.timestamp >= start)

    if end is not None:
        query = query.filter(Report.timestamp <= end)

    query = (
        query.order_by(Report.timestamp.desc()).limit(limit).offset((page - 1) * limit)
    )

    return query.all()


def get_by_id(report_id: int, db: Session) -> Report:
    """Get report by ID."""

    report: Union[Report, None] = db.query(Report).get(report_id)

    if not report:
        raise HTTPException(
            status_code=404,
            detail=f"Report with ID {report_id} not found",
        )

    return report


def create(report: Report, db: Session) -> Report:
    """Create a new report."""

    db.add(report)
    db.commit()

    return report


def update(report_id: UUID, updated_report: Report, db: Session) -> Report:
    """Update a report."""

    current_report = get_by_id(report_id, db)

    current_report.notes = updated_report.notes
    current_report.person_responsible = updated_report.person_responsible
    current_report.is_closed = updated_report.is_closed
    db.add(current_report)
    db.commit()

    return current_report


def get_chart(
    start: Union[datetime, None],
    end: Union[datetime, None],
    db: Session,
) -> List:
    """Get all report as a chart data."""

    query = db.query(
        func.DATE(Report.timestamp),
        func.unnest(Report.reason),
        func.count(Report.reason),
    )

    if start:
        query = query.filter(Report.timestamp >= start)

    if end:
        query = query.filter(Report.timestamp <= end)

    result = (
        query.group_by(func.DATE(Report.timestamp), Report.reason)
        .order_by(func.DATE(Report.timestamp), Report.reason)
        .all()
    )

    charts = {}
    for row in result:
        reason_name: str = sub("[-\s]", "_", row[1]).lower()
        reasons: dict = charts.get(row[0], {})
        reasons[reason_name] = row[2]
        charts[row[0]] = reasons

    return [{key: value} for key, value in charts.items()]


async def save_image(image_base64: str, filename: str, current_date: str) -> None:
    """Decode base64 image and save to static folder"""

    try:
        image_content = b64decode(image_base64.encode("utf-8"))
        folder_path = os.path.join(STATIC_ROOT, current_date)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        filepath = os.path.join(folder_path, filename)
        async with aiofiles.open(filepath, "wb") as out_file:
            await out_file.write(image_content)
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
