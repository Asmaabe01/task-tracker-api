from enum import Enum

from sqlmodel import SQLModel, Field, Relationship



class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    
class TaskBase(SQLModel):
    title: str
    completed: bool = False
    priority: Priority = Priority.medium


class Task(TaskBase, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="user.id"
    )

    user: "User" = Relationship(
        back_populates="tasks"
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    completed: bool | None = None
    priority: Priority | None = None


