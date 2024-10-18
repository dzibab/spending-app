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


# Serve the index.html for the root path
@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("frontend/index.html") as f:
        return f.read()


@app.get("/auth", response_class=HTMLResponse)
async def read_auth_page():
    with open("frontend/auth.html") as f:
        return f.read()


@app.get("/add-spending", response_class=HTMLResponse)
async def read_add_spending_page():
    with open("frontend/add_spending.html") as f:
        return f.read()
