from fastapi import APIRouter, WebSocket

from app.library.kafka_consumer_lib import consume_messages


router = APIRouter(prefix="/camera", tags=["Camera"])

websocket_connections = set()


@router.websocket("/{camera_id}")
async def websocket_endpoint(websocket: WebSocket, camera_id: str):
    await websocket.accept()
    websocket_connections.add((camera_id, websocket))
    try:
        await consume_messages(camera_id, websocket_connections)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        websocket_connections.remove((camera_id, websocket))