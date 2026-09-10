from sqlmodel import SQLModel, Field, Relationship


class TaskBase(SQLModel):
    title: str
    completed: bool = False


class Task(TaskBase, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    user_id: int | None = Field(
        default=None,
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