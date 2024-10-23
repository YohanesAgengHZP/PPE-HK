"""
Database models.
"""

from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List, Optional


DEFAULT_ARRAY_TEXT = "'{}'::text[]"


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
    tags: Mapped[List[str]] = mapped_column(
        ARRAY(Text),
        server_default=text(DEFAULT_ARRAY_TEXT),
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
    - photo: URL of the employee photo
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
    - photo: URL of the photo taken when employee has start or leave work
    - work_status: Work status, true for start work and false for leave work
    - camera_name: Camera name where the attendance is captured
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
    camera_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Camera name where the attendance is captured",
    )

    def __repr__(self) -> str:
        time_format = "%d %b %Y %H:%M:%S"
        time = datetime.strftime(self.time, time_format)
        return f"EmployeeAttendance(id={self.id!r}, employee_id={self.employee_id!r}, time={time}, work_status={self.work_status})"


class Report(Base):
    """
    Report violation table.

    ### Variable:
    - id: Report ID
    - timestamp: Timestamp when the violation occured
    - reason: Reason of the violation
    - image_url: URL of the image when violation occured
    - camera_name: Camera name where the violation is captured
    - notes: Notes for the violation
    - person_responsible: Name of the person responsible for handling the violation
    - is_closed: Status for the vilation
    - num_of_people: Number of people detected of violation
    - people_without_ppe_id: ID of the people doing violation
    """

    __tablename__ = "reporting"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        doc="Report ID",
    )
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        doc="Timestamp when the violation occured",
    )
    reason: Mapped[List[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default=text(DEFAULT_ARRAY_TEXT),
        doc="Reason of the violation",
    )
    image_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="URL of the image when violation occured",
    )
    camera_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Camera name where the violation is captured",
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        doc="Notes for the violation",
    )
    person_responsible: Mapped[Optional[str]] = mapped_column(
        Text,
        doc="Name of the person responsible for handling the violation",
    )
    is_closed: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        doc="Status for the vilation",
    )
    num_of_people: Mapped[Optional[int]] = mapped_column(
        Integer,
        doc="Number of people detected of violation",
    )
    people_without_ppe_id: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(Text),
        doc="ID of the people doing violation",
    )

    def __repr__(self):
        time_format = "%d %b %Y %H:%M:%S"
        timestamp = datetime.strftime(self.timestamp, time_format)
        return f"Report(id={self.id!r}, timestamp={timestamp!r}, reason={self.reason!r}, image_url={self.image_url!r}, camera_name={self.camera_name!r})"
