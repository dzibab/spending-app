import aiofiles
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from .db.session import Base, engine
from .routes import spending, auth


app = FastAPI()


# Create the database tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(spending.router)
app.include_router(auth.router)


# Mount the static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index():
    async with aiofiles.open("frontend/index.html") as f:  # Use aiofiles for async file I/O
        return await f.read()


@app.get("/auth", response_class=HTMLResponse)
async def read_auth_page():
    async with aiofiles.open("frontend/auth.html") as f:
        return await f.read()


@app.get("/add-spending", response_class=HTMLResponse)
async def read_add_spending_page():
    async with aiofiles.open("frontend/add_spending.html") as f:
        return await f.read()
