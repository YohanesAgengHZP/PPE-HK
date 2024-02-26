import cv2
import numpy as np
import websocket
import threading

# Function to handle incoming WebSocket messages
def on_message(ws, message):

    frame = np.frombuffer(message, dtype=np.uint8)

    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow("Received Frame", img)
    cv2.waitKey(1)  


def on_open(ws):
    print("WebSocket connected")


def on_close(ws):
    print("WebSocket closed")

if __name__ == "__main__":
    ws_url = "ws://localhost:9005/video"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_open=on_open, on_close=on_close)
    threading.Thread(target=ws.run_forever).start()
    while True:
        pass
