from fastapi import FastAPI

from app.routers import users, tasks


app = FastAPI()


app.include_router(users.router)
app.include_router(tasks.router)



@app.get("/")
def home():
    return {
        "message": "Welcome to my Task Tracker API"
    }