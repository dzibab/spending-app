from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers.spending import router as spending_router
from src.db.session import engine
from src.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(spending_router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
