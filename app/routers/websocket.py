from fastapi import WebSocket, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Ini hasil pesannya yang dikirim nih : {data}")
