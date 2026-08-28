import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta, timezone
import jwt
from app.config.secretes import secretes
import pytest_asyncio
from app.main import app
from unittest.mock import MagicMock, AsyncMock
from app.config.database import get_db

TEST_SECRET_KEY = secretes.JWT_SECRET_KEY
TEST_ALGORITHM = secretes.JWT_ALGORITHM
TEST_USER_ID = 123

@pytest_asyncio.fixture
async def mock_db():
    db = MagicMock()

    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()

    return db

@pytest.fixture
def test_token():
    payload = {
        "user_id": TEST_USER_ID,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(
        payload,
        TEST_SECRET_KEY,
        algorithm=TEST_ALGORITHM,
    )


@pytest_asyncio.fixture
async def authenticated_client(test_token, mock_db):
    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={
            "Authorization": f"Bearer {test_token}"
        },
    ) as client:
        yield client

    app.dependency_overrides.clear()