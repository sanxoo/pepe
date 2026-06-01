from httpx import AsyncClient, ASGITransport
from main import app

import pytest
import dotenv
import os
import db

dotenv.load_dotenv()


@pytest.fixture(scope="module")
async def db_conn():
    await db.connect()
    yield
    await db.disconn()


@pytest.mark.anyio
async def test_insert(db_conn):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000/api/v1"
    ) as ac:
        response = await ac.post(
            "users",
            headers={"X-API-Key": os.getenv("API_KEY")},
            json={"mail": "sanxoo", "name": "sanxoo"},
        )
    assert response.status_code == 200
    assert response.json() == {"mail": "sanxoo", "name": "sanxoo"}


@pytest.mark.anyio
async def test_get(db_conn):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000/api/v1"
    ) as ac:
        response = await ac.get(
            "users/sanxoo", headers={"X-API-Key": os.getenv("API_KEY")}
        )
    assert response.status_code == 200
    assert response.json() == {"mail": "sanxoo", "name": "sanxoo"}
