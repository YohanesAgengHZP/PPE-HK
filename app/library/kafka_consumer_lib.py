import asyncio
import os

from dotenv import load_dotenv
from kafka import KafkaConsumer


load_dotenv()
lock = asyncio.Lock()

consumer = KafkaConsumer(
    os.getenv("TOPIC_KAFKA"),
    bootstrap_servers=[os.getenv("KAFKA_URL")],
    api_version=(0, 10, 2),
)


async def consume_messages(camera_id: str, websocket_connections):
    while True:
        for msgs in consumer.poll(max_records=1).values():
            for msg in msgs:
                await process_message(msg, camera_id, websocket_connections)
        await asyncio.sleep(0.05)


async def process_message(msg, camera_id_ws, websocket_connections):
    camera_id = msg.key.decode("utf-8")
    if camera_id == camera_id_ws:
        encoded_frame = msg.value
        async with lock:
            await asyncio.gather(
                *[
                    connection[1].send_bytes(encoded_frame)
                    for connection in websocket_connections
                    if connection[0] == camera_id
                ]
            )
