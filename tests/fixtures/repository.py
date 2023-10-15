import pytest

from src.config import AppSettings
from src.repository import (
    aws,
    file,
    web,
)


@pytest.fixture
async def aws_repo(s3_client, test_settings: AppSettings):
    yield aws.Repository(
        s3_client=s3_client,
        bucket_name=test_settings.S3_BUCKET_NAME,
    )


@pytest.fixture
def file_repo(test_settings: AppSettings):
    repo = file.create(config=test_settings)
    yield repo


@pytest.fixture
def web_repo(test_settings: AppSettings):
    repo = web.create(config=test_settings)
    yield repo
