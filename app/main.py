from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import users, tasks


app = FastAPI()


app.include_router(users.router)
app.include_router(tasks.router)


@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {
        "message": "Welcome to my Task Tracker API"
    }