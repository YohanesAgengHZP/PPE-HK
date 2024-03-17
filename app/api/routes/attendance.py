from fastapi import APIRouter


router = APIRouter(prefix="/attendance", tags=["Employee", "Attendance"])


# TODO: Implement get all attendance function
@router.get("")
async def get_all_attendance():
    pass
