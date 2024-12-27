from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.spending import router as spending_router
from backend.routers.currency import router as currency_router
from backend.routers.category import router as category_router
from backend.routers.user import router as user_router
from backend.routers.auth import router as auth_router
from backend.db.session import async_session, engine, initialize_default_data
from backend.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as db:
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await initialize_default_data(db)

        yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(spending_router, prefix="/api")
app.include_router(currency_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
