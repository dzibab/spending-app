from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers.spending import router as spending_router
from src.db.db import database
from src.db.session import async_session
from src.db.models import Base


app = FastAPI()
app.include_router(spending_router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    async with async_session() as session:
        async with session.begin():
            await session.run_sync(Base.metadata.create_all)
    yield
    await database.disconnect()
