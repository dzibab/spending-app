from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.routers.spending import router as spending_router
from backend.routers.currency import router as currency_router
from backend.routers.category import router as category_router
from backend.routers.user import router as user_router
from backend.db.session import async_session, engine, initialize_default_data
from backend.db.models import Base


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


# Routers
app.include_router(spending_router)
app.include_router(currency_router)
app.include_router(category_router)
app.include_router(user_router)
