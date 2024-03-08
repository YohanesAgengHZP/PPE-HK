import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from routes import routers, routers_ws
from fastapi.middleware.cors import CORSMiddleware
# from library.kafka_consumer_lib import consume_messages

load_dotenv()

app = FastAPI()

origins = ['http://127.0.0.1:9090']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Call Router
app.include_router(routers.router)
app.include_router(routers_ws.router)

async def run_app():
    await asyncio.gather(app())

if __name__ == "__main__":
    asyncio.run(run_app())
