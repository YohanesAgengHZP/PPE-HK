import threading
from flask import Flask, Response
from kafka import KafkaConsumer

# Fire up the Kafka Consumer
topic = "yolo_camera"
consumer = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"])

# Set up a flag to control the consumer loop
consumer_running = True

# Set the consumer in a Flask App
app = Flask(__name__)


@app.route("/video", methods=["GET"])
def video():
    """
    This is the heart of our video display. Notice we set the mimetype to
    multipart/x-mixed-replace. This tells Flask to replace any old images with
    new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


def kafka_consumer_thread():
    """
    This function runs in a separate thread and continuously consumes messages
    from the Kafka topic.
    """
    global consumer_running
    try:
        for msg in consumer:
            if not consumer_running:
                break
            yield (
                b"--frame\r\n" b"Content-Type: image/jpg\r\n\r\n" + msg.value + b"\r\n\r\n"
            )
    except Exception as e:
        print("Error in Kafka consumer thread:", e)


def get_video_stream():
    """
    This function starts the Kafka consumer thread and yields the received frames.
    """
    return kafka_consumer_thread()


@app.route("/stop")
def stop_consumer():
    """
    This endpoint stops the Kafka consumer loop.
    """
    global consumer_running
    consumer_running = False
    return "Kafka consumer stopped."


if __name__ == "__main__":
    # Start Kafka consumer thread
    consumer_thread = threading.Thread(target=kafka_consumer_thread)
    consumer_thread.daemon = True
    consumer_thread.start()

    # Run Flask app
    app.run(host="0.0.0.0", port=9005, debug=True)