from datetime import datetime
from fastapi import HTTPException
from re import sub
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Literal, Tuple, Union
from uuid import UUID

from core.models import Camera, Report


PPE_CLASS_NAME_LIST = ["NO-Hardhat", "NO-Safety Shoes", "NO-Safety Vest"]
DANGER_CLASS_NAME_LIST = ["Fire", "Puddle", "Smoke", "Smoking"]


def get_all(
    type: Union[Literal["ppe", "danger"] | None],
    tags: Union[List[str], None],
    reasons: Union[List[str], None],
    start: Union[datetime, None],
    end: Union[datetime, None],
    limit: int,
    page: int,
    db: Session,
) -> Tuple[int, List[Report]]:
    """
    Get all reports. Filter are optional.

    Type are prioritized over reasons.

    Can filter based on list of camera tags.

    Returns:
        results (Tuple[int, List[Report]]): a tuple of total number of records and the results per page.
    """

    count_query = db.query(func.count(Report.id)).join(
        Camera, Report.camera_name == Camera.name
    )
    query = db.query(Report).join(Camera, Report.camera_name == Camera.name)

    if tags:
        count_query = count_query.filter(Camera.tags.overlap(tags))
        query = query.filter(Camera.tags.overlap(tags))

    if type:
        match type:
            case "danger":
                count_query = count_query.filter(
                    Report.reason.overlap(DANGER_CLASS_NAME_LIST)
                )
                query = query.filter(Report.reason.overlap(DANGER_CLASS_NAME_LIST))
            case "ppe":
                count_query = count_query.filter(
                    Report.reason.overlap(PPE_CLASS_NAME_LIST)
                )
                query = query.filter(Report.reason.overlap(PPE_CLASS_NAME_LIST))
    elif reasons:
        count_query = count_query.filter(Report.reason.overlap(reasons))
        query = query.filter(Report.reason.overlap(reasons))

    if start is not None:
        count_query = count_query.filter(Report.timestamp >= start)
        query = query.filter(Report.timestamp >= start)

    if end is not None:
        count_query = count_query.filter(Report.timestamp <= end)
        query = query.filter(Report.timestamp <= end)

    if limit <= 0:
        limit = 10

    if page <= 0:
        page = 1

    count = count_query.scalar()
    result = (
        query.order_by(Report.timestamp.desc())
        .limit(limit)
        .offset((page - 1) * limit)
        .all()
    )

    return count, result


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


def count_all(db: Session) -> int:
    """Count all records."""

    return db.query(func.count(Report.id)).scalar()
