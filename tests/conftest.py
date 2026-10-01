import pytest

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.main import app
from app.database import get_session


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


def get_test_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(autouse=True)
def reset_database():
    SQLModel.metadata.create_all(test_engine)

    yield

    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def client():
    return TestClient(app)