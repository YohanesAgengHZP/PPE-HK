# import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api


load_dotenv()

app = FastAPI()

origins = ["http://127.0.0.1:9090"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(api.router)


# async def run_app():
#     await asyncio.gather(app())


# if __name__ == "__main__":
#     asyncio.run(run_app())