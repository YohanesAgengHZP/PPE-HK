from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Union
from uuid import UUID

from core.models import Report


def get_all(
    search: Union[List[str], None],
    start: Union[datetime, None],
    end: Union[datetime, None],
    limit: int,
    page: int,
    db: Session,
) -> List[Report]:
    """Get all reports. Filter are optional."""

    query = db.query(Report)

    if search:
        query = query.filter(Report.reason.any(search))

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


# TODO: Change the raw sql statement to ORM
def get_chart(start: datetime, end: datetime, db: Session) -> List:
    """Get all report as a chart data."""

    # subquery = (
    #     db.query(
    #         func.to_char(Report.timestamp, "dd").label("formatted_date"),
    #         func.unnest(Report.reason).label("reason"),
    #     )
    #     .filter(Report.timestamp.between(start, end))
    #     .subquery("subquery")
    # )
    # return (
    #     db.query(
    #         "formatted_date",
    #         func.sum(
    #             case(
    #                 (func.lower(Report.reason).like("%no-hardhat%"), 1),
    #                 else_=0,
    #             )
    #         ).label("no_hardhat_count"),
    #         func.sum(
    #             case(
    #                 (func.lower(Report.reason).like("%no-safety shoe%"), 1),
    #                 else_=0,
    #             )
    #         ).label("no_safety_shoe_count"),
    #         func.sum(
    #             case(
    #                 (func.lower(Report.reason).like("%no-safety vest%"), 1),
    #                 else_=0,
    #             )
    #         ).label("no_safety_vest_count"),
    #     )
    #     .from_statement(subquery)
    #     .group_by("formatted_date")
    #     .order_by("formatted_date")
    #     .all()
    # )
    sql = text(
        f"""SELECT formatted_date,
                SUM(CASE WHEN lower(reason) LIKE '%no-hardhat%' THEN 1 ELSE 0 END) AS no_hardhat_count,
                SUM(CASE WHEN lower(reason) LIKE '%no-safety shoe%' THEN 1 ELSE 0 END) AS no_safety_shoe_count,
                SUM(CASE WHEN lower(reason) LIKE '%no-safety vest%' THEN 1 ELSE 0 END) AS no_safety_vest_count
                FROM (
                    SELECT TO_CHAR("timestamp"::date, 'dd') AS formatted_date, unnest(reason) AS reason
                    FROM reporting
                    WHERE date("timestamp") BETWEEN '{start}' and '{end}'
                ) AS subquery
                GROUP BY formatted_date ORDER BY formatted_date"""
    )
    result = db.execute(sql)
    return [report._asdict() for report in result.all()]
