import pytest

from src.config import AppSettings
from src.clients.aws import s3


@pytest.fixture
async def s3_client(test_settings: AppSettings):
    client = await s3.create(config=test_settings)
    yield client
