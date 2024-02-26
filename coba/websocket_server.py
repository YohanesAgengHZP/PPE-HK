from kafka import KafkaConsumer
import numpy as np
import cv2
import time
from flask import Flask, Response
from flask_sockets import Sockets

topic = "yolo_camera"

consumer = KafkaConsumer(topic, bootstrap_servers=["localhost:19092"])

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/video')
def video_socket(ws):
    try:
        print('WebSocket connected')
        for msg in consumer:
            encoded_frame = msg.value
            camera_id = msg.key.decode()  


            if len(encoded_frame) > 9999:
                i = np.frombuffer(encoded_frame, dtype=np.uint8)
                im = cv2.imdecode(i, cv2.IMREAD_UNCHANGED)

                _, frame = cv2.imencode('.png', im)
                frame_bytes = frame.tobytes()


                ws.send(frame_bytes)

 
                print(f"Sent YOLO frame from camera {camera_id} with length:", len(frame_bytes))

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=9005, debug=True, use_reloader=False)
