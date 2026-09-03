from contextlib import asynccontextmanager
from typing import Literal
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pwdlib import PasswordHash
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ---------------- 1. Database Models ----------------
# Here we define the tables that will exist in our database.
# Task = task table
# User = user table

class TaskBase(SQLModel):
    title: str
    completed: bool = False


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    completed: bool | None = None


class UserCreate(SQLModel):
    username: str
    password: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str


class UserPublic(SQLModel):
    id: int
    username: str


# ---------------- 2. Database Connection ----------------
# Here we create the connection between FastAPI and SQLite database.
# tasks.db is where our data is stored.

sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False}
)

# ---------------- 3. Authentication System ----------------
# This section handles:
# - password encryption
# - creating JWT tokens
# - checking if a user is logged in

password_hash = PasswordHash.recommended()

SECRET_KEY = "temporary-learning-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password
    )

def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    statement = select(User).where(
        User.username == username
    )

    db_user = session.exec(statement).first()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return db_user


# ---------------- Endpoints ----------------

@app.get("/")
def home():
    return {
        "message": "Welcome to my Task Tracker API"
    }


# ---------------- User Authentication Endpoints ----------------
# Register creates a new user.
# Login checks username/password.
# Successful login gives a JWT token.

@app.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    statement = select(User).where(
        User.username == user.username
    )

    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    hashed = hash_password(user.password)

    db_user = User(
        username=user.username,
        hashed_password=hashed
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    statement = select(User).where(
        User.username == form_data.username
    )

    db_user = session.exec(statement).first()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(db_user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ---------------- Task CRUD Endpoints ----------------
# CRUD means:
# Create  -> POST /tasks
# Read    -> GET /tasks
# Update  -> PUT/PATCH /tasks/{id}
# Delete  -> DELETE /tasks/{id}

@app.get("/tasks", response_model=list[Task])
def get_tasks(
    completed: bool | None = None,
    search: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort: Literal["asc", "desc"] = "asc",
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Task)

    if completed is not None:
        statement = statement.where(
            Task.completed == completed
        )

    if search:
        statement = statement.where(
            Task.title.contains(search)
        )

    if sort == "desc":
        statement = statement.order_by(Task.id.desc())
    else:
        statement = statement.order_by(Task.id.asc())

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
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    print("TASK RECEIVED:", task)
    print("CURRENT USER:", current_user)


    db_task = Task(
    title=task.title,
    completed=task.completed,
    user_id=current_user.id
)

    print("DATABASE TASK:", db_task)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    print(db_task)

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


@app.patch("/tasks/{task_id}", response_model=Task)
def patch_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_update.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    db_task.sqlmodel_update(update_data)

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