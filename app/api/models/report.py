from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from api.models.common import Base64File


class ReportBase(BaseModel):
    timestamp: datetime
    reason: List[str]
    image_url: str
    camera_name: str
    notes: Optional[str]
    person_responsible: Optional[str]
    is_closed: Optional[bool]
    num_of_people: Optional[int]
    people_without_ppe_id: Optional[List[str]]


class ReportResponse(ReportBase):
    id: int


class ReportCreate(BaseModel):
    timestamp: datetime
    reason: List[str]
    image: Base64File
    camera_name: str
    num_of_people: Optional[int]
    people_without_ppe_id: Optional[List[str]]


class ReportUpdate(BaseModel):
    notes: Optional[str]
    person_responsible: Optional[str]
    is_closed: Optional[bool]
