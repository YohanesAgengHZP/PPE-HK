"""
Database models.
"""

from datetime import datetime
from sqlalchemy import ARRAY, Boolean, DateTime, ForeignKey, Integer, Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


class Camera(Base):
    """
    Camera information table.

    ### Variable:
    - id: Camera ID
    - name: Name of the camera
    - url: URL of the camera
    - active: Camera active status
    - tags: Tags that are assigned to the camera
    """

    __tablename__ = "camera"

    id: Mapped[Uuid] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
        doc="Camera ID",
    )
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Name of the camera",
    )
    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="URL of the camera",
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
        doc="Camera active status",
    )
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        server_default=text("'{}'::text[]"),
        doc="Tags that are assigned to the camera",
    )

    def __repr__(self) -> str:
        return f"Camera(id={self.id!r}, name={self.name!r}, url={self.url!r}, active={self.active}, tags={self.tags!r})"


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
        Text,
        nullable=False,
        doc="Name of the employee",
    )
    company: Mapped[str] = mapped_column(
        Text,
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
        Text,
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
        Text,
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
