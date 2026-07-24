from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    title: str
    completed: bool = False


tasks = []


@app.get("/")
def home():
    return {"message": "Welcome to my Task Tracker API"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }

    tasks.append(new_task)
    return new_task