from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ---------------- Models ----------------

class TaskBase(SQLModel):
    title: str
    completed: bool = False


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


# ---------------- Database ----------------

sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# ---------------- Endpoints ----------------

@app.get("/")
def home():
    return {"message": "Welcome to my Task Tracker API"}


@app.get("/tasks", response_model=list[Task])
def get_tasks(
    completed: bool | None = None,
    search: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    statement = select(Task)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    if search:
        statement = statement.where(Task.title.contains(search))

    statement = statement.offset(offset).limit(limit)

    tasks = session.exec(statement).all()
    return tasks




@app.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    db_task = Task.model_validate(task)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db_task.title = updated_task.title
    db_task.completed = updated_task.completed

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = {
        "id": db_task.id,
        "title": db_task.title,
        "completed": db_task.completed
    }

    session.delete(db_task)
    session.commit()

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }