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
        server_default=text(""),
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
    - start: Employee start work date time
    - end: Employee leave work date time
    - start_photo: Photo taken when employee start work
    - end_photo: Photo taken when employee leave work
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
    start: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        doc="Employee start work date time",
    )
    end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        doc="Employee leave work date time",
    )
    start_photo: Mapped[Optional[str]] = mapped_column(
        String,
        doc="Photo taken when employee start work",
    )
    end_photo: Mapped[Optional[str]] = mapped_column(
        String,
        doc="Photo taken when employee leave work",
    )

    def __repr__(self) -> str:
        time_format = "%d %b %Y %H:%M:%S"
        start_string = datetime.strftime(self.start, time_format)
        end_string = datetime.strftime(self.end, time_format)
        return f"EmployeeAttendance(id={self.id!r}, employee_id={self.employee_id!r}, start={start_string}, end={end_string})"
