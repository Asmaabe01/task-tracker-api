from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to my Task Tracker API"}