from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get('/')
async def get():
  item = {'message' : 'Hello World'}
  return JSONResponse(content=item, status_code=200)
