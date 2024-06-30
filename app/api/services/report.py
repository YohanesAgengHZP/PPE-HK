from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import case, func
from typing import List
from uuid import UUID

from core.models import Report


def get_all(db: Session) -> List[Report]:
    """Get all reports."""

    return db.query(Report).all()


def get_by_id(report_id: int, db: Session) -> Report:
    """Get report by ID."""

    report: Report = db.query(Report).get(report_id)

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

    if not current_report:
        raise HTTPException(
            status_code=404,
            detail=f"Report with ID {report_id} not found",
        )

    current_report.notes = updated_report.notes
    current_report.person_responsible = updated_report.person_responsible
    current_report.is_closed = updated_report.is_closed
    db.add(current_report)
    db.commit()

    return updated_report
