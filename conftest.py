import pytest
from hockey_stat.storage.database import SessionLocal


@pytest.fixture(scope="function")
def get_db():
    """Sync DB сессия для тестов"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def client():
    """HTTP клиент мок"""
    return "mocked html"


def read_file(filename: str) -> str:
    with open(filename, "r") as fp:
        return fp.read()
