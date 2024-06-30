from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReportBase(BaseModel):
    timestamp: datetime
    reason: list[str]
    image_url: str
    camera_name: str
    notes: str
    person_responsible: str
    is_closed: bool
    num_of_people: int
    people_without_ppe_id: list[str]


class ReportResponse(ReportBase):
    id: int


class ReportCreate(BaseModel):
    reason: list[str]
    image_url: Optional[str]
    camera_name: str
    num_of_people: Optional[int]
    people_without_ppe_id: Optional[list[str]]


class ReportUpdate(BaseModel):
    notes: Optional[str]
    person_responsible: Optional[str]
    is_closed: Optional[bool]
