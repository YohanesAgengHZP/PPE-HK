"""
Database models.
"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


class Employee(Base):
    """
    Employee information table.

    ### Variable:
    - id: Employee ID
    - name: Name of the employee
    - company: Company where the employee is currently working
    - mcu: Employee active medical check up status
    - photo: Employee photo
    """

    __tablename__ = "employee"

    id: Mapped[Uuid] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
        doc="Employee ID",
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Name of the employee",
    )
    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Company where the employee is currently working",
    )
    mcu: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
        doc="Employee active medical check up status",
    )
    photo: Mapped[str] = mapped_column(
        String,
        nullable=False,
        doc="Employee photo",
    )

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, name={self.name!r}, compay={self.company!r}, mcu={self.mcu}, photo={self.photo!r})"


class EmployeeAttendance(Base):
    """
    Employee attendance table.

    ### Variable:
    - id: Attendance ID
    - employee_id: The employee ID
    - time: Employee attendance date time
    - photo: Photo taken when employee has start or leave work
    - work_status: Work status, true for start work and false for leave work
    """

    __tablename__ = "employee_attendance"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        doc="Attendance ID",
    )
    employee_id: Mapped[Uuid] = mapped_column(
        ForeignKey("employee.id"),
        nullable=False,
        doc="The employee ID",
    )
    time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        doc="Employee attendance date time",
    )
    photo: Mapped[Optional[str]] = mapped_column(
        String,
        doc="Photo taken when employee has start or leave work",
    )
    work_status: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
        doc="Work status, true for start work and false for leave work",
    )

    def __repr__(self) -> str:
        time_format = "%d %b %Y %H:%M:%S"
        time = datetime.strftime(self.time, time_format)
        return f"EmployeeAttendance(id={self.id!r}, employee_id={self.employee_id!r}, time={time}, work_status={self.work_status})"
