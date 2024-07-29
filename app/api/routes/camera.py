from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Union
from uuid import UUID

from api.dependencies import get_db
from api.models.camera import (
    CameraActiveStatus,
    CameraCreate,
    CameraResponse,
    CameraUpdate,
)
from api.services.camera import get_all, get_by_id, create, update, delete
from core.models import Camera


router = APIRouter(prefix="/camera", tags=["Camera"])


@router.get("", response_model=List[CameraResponse])
async def get_all_camera(
    name: Union[str, None] = None,
    tags: Union[str, None] = None,
    active: Union[bool, None] = None,
    db: Session = Depends(get_db),
):
    tag_array = tags.split(",") if tags else None
    return get_all(name, tag_array, active, db)


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: UUID, db: Session = Depends(get_db)):
    return get_by_id(camera_id, db)


@router.post("", status_code=201, response_model=CameraResponse)
async def create_camera(new_camera: CameraCreate, db: Session = Depends(get_db)):
    camera = Camera()
    camera.name = new_camera.name
    camera.url = new_camera.url
    camera.active = new_camera.active
    camera.tags = new_camera.tags

    return create(camera, db)


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: UUID, updated_camera: CameraUpdate, db: Session = Depends(get_db)
):
    camera = Camera()
    camera.name = updated_camera.name
    camera.url = updated_camera.url
    camera.active = updated_camera.active
    camera.tags = updated_camera.tags

    return update(camera_id, camera, db)


@router.delete("/{camera_id}", status_code=204, response_model=None)
async def delete_camera(camera_id: UUID, db: Session = Depends(get_db)):
    return delete(camera_id, db)


@router.post("/{camera_id}/status", status_code=204, response_model=None)
async def update_camera_active_status(
    camera_id: UUID, active: CameraActiveStatus, db: Session = Depends(get_db)
):
    """Activate or deactivate camera."""

    camera = get_by_id(camera_id, db)
    camera.active = active.active
    update(camera_id, camera, db)

    return None
