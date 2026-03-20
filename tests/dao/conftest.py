import pytest

from hockey_stat.storage.middleware import SessionLocal


@pytest.fixture(scope="function")
async def get_async_db():
    async with SessionLocal() as session:
        yield session
