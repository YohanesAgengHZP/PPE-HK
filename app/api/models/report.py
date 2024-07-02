from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class ReportBase(BaseModel):
    timestamp: datetime
    reason: List[str]
    image_url: str
    camera_name: str
    notes: str
    person_responsible: str
    is_closed: bool
    num_of_people: int
    people_without_ppe_id: List[str]


class ReportResponse(ReportBase):
    id: int


class ReportCreate(BaseModel):
    reason: List[str]
    image_url: Optional[str]
    camera_name: str
    num_of_people: Optional[int]
    people_without_ppe_id: Optional[List[str]]


class ReportUpdate(BaseModel):
    notes: Optional[str]
    person_responsible: Optional[str]
    is_closed: Optional[bool]
