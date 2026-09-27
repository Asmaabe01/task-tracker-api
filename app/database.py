from sqlmodel import Session, create_engine


sqlite_file_name = "tasks.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={
        "check_same_thread": False
    }
)


def get_session():
    with Session(engine) as session:
        yield session