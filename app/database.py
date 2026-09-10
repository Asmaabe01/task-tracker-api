from sqlmodel import SQLModel, Session, create_engine


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