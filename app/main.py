from fastapi import FastAPI


from .db.session import Base, engine
from .routes import spending

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(spending.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Spending Tracker!"}
