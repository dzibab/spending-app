from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers.spending import router as spending_router
from src.db.session import async_session, engine, initialize_default_data
from src.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Get the engine directly
    async with async_session() as db:
        # Create tables
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # Initialize default categories and currencies
        await initialize_default_data(db)
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(spending_router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
