"""
Main API endpoint.
"""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.api.routes import attendance, camera, employee


router = APIRouter()

router.include_router(attendance.router)
router.include_router(camera.router)
router.include_router(employee.router)


@router.get("/", response_class=PlainTextResponse, tags="Check")
def check():
    """Give response if server is up."""
    return """
 ______________________________
< Hello, welcome to the server >
 ------------------------------
        \ | ^__^
         \| (OO)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||
"""
