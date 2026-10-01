from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User
from app.security import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@router.post("/")
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    new_task = Task(
    title=task.title,
    completed=task.completed,
    priority=task.priority,
    user_id=current_user.id
)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task



@router.get("/")
def get_tasks(
    completed: bool | None = None,
    priority: str | None = None,
    page: int = 1,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    statement = select(Task).where(
        Task.user_id == current_user.id
    )

    if completed is not None:
        statement = statement.where(
            Task.completed == completed
        )

    if priority is not None:
        statement = statement.where(
            Task.priority == priority
        )

    offset = (page - 1) * limit

    statement = statement.offset(offset).limit(limit)

    tasks = session.exec(statement).all()

    return tasks



@router.get("/{task_id}")
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    task = session.get(Task, task_id)


    if task is None or task.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task



@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    task = session.get(Task, task_id)


    if task is None or task.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    task_data = task_update.model_dump(
        exclude_unset=True
    )


    for key, value in task_data.items():
        setattr(task, key, value)


    session.add(task)
    session.commit()
    session.refresh(task)

    return task



@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    task = session.get(Task, task_id)


    if task is None or task.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    session.delete(task)
    session.commit()


    return {
        "message": "Task deleted"
    }