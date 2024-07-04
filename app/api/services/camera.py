from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Union
from uuid import UUID

from core.models import Camera


def get_all(
    name: Union[str, None],
    tags: Union[List[str], None],
    active: Union[bool, None],
    db: Session,
) -> List[Camera]:
    """Get all cameras. Filter are optional."""

    query = db.query(Camera)
    if name:
        query = query.filter(Camera.name.ilike(f"%{name}%"))
    if tags:
        query = query.filter(Camera.tags.any(str(tags)))
    if active is not None:
        query = query.filter(Camera.active == active)
    return query.all()


def get_by_id(camera_id: UUID, db: Session) -> Camera:
    """Get camera by ID."""

    camera: Camera = db.query(Camera).get(camera_id)

    if not camera:
        raise HTTPException(
            status_code=404,
            detail=f"Camera with ID {camera_id} not found",
        )

    return camera


def create(camera: Camera, db: Session) -> Camera:
    """Create a new camera."""

    db.add(camera)
    db.commit()

    return camera


def update(camera_id: UUID, updated_camera: Camera, db: Session) -> Camera:
    """Update a camera."""

    current_camera = get_by_id(camera_id, db)

    if not current_camera:
        raise HTTPException(
            status_code=404,
            detail=f"Camera with ID {camera_id} not found",
        )

    current_camera.name = updated_camera.name
    current_camera.url = updated_camera.url
    current_camera.active = updated_camera.active
    current_camera.tags = updated_camera.tags
    db.add(current_camera)
    db.commit()

    return updated_camera


def delete(camera_id: UUID, db: Session) -> None:
    """Delete a camera."""

    camera = db.query(Camera).get(camera_id)

    if not camera:
        raise HTTPException(
            status_code=404,
            detail=f"Camera with ID {camera_id} not found",
        )

    db.delete(camera)
    db.commit()
