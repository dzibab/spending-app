from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .db.session import Base, engine, get_db
from .routes import spending, auth
from .routes.spending import get_spendings


app = FastAPI()
templates = Jinja2Templates(directory="frontend")


# Create the database tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(spending.router)
app.include_router(auth.router)


# Mount the static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    content = "<h1>Welcome to the Spending Tracker!</h1>"
    return templates.TemplateResponse(request, "main.html", {"content": content})


@app.get("/auth", response_class=HTMLResponse)
async def read_auth_page(request: Request):
    content = """
        <h1>Login</h1>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    """
    return templates.TemplateResponse("main.html", {"request": request, "content": content})


@app.get("/add-spending", response_class=HTMLResponse)
async def read_add_spending_page(request: Request):
    content = """
        <h1>Add Spending</h1>
        <form action="/spendings" method="post">
            <input type="text" name="description" placeholder="Description" optional>
            <input type="number" name="amount" placeholder="Amount" step="0.01" required>
            <input type="date" name="date" required>
            <input type="text" name="currency" placeholder="Currency" required>
            <input type="text" name="category" placeholder="Category" required>
            <button type="submit">Add Spending</button>
        </form>
    """
    return templates.TemplateResponse("main.html", {"request": request, "content": content})


@app.get("/spendings", response_class=HTMLResponse)
async def read_spendings(request: Request, db: Session = Depends(get_db)):
    # Call the get_spendings function with default parameters
    spendings_response = get_spendings(skip=0, limit=1000, db=db)  # Adjust limit as needed

    # Extract the spendings from the response
    spendings = spendings_response['spendings']

    # Build the HTML content
    content = "<h1>Your Spendings</h1><ul>"
    for s in spendings:
        content += f"<li>{s.description} - {s.amount} {s.currency} on {s.date}</li>"
    content += "</ul>"

    return templates.TemplateResponse("main.html", {"request": request, "content": content})
