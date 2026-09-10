from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    username: str = Field(index=True)

    hashed_password: str

    tasks: list["Task"] = Relationship(
        back_populates="user"
    )


class UserCreate(SQLModel):
    username: str
    password: str


class UserPublic(SQLModel):
    id: int
    username: str