from functools import lru_cache

import dotenv
from pydantic import (
    BaseSettings,
    SecretStr,
)


class AppSettings(BaseSettings):
    AWS_KEY: str = ""
    AWS_SECRET_KEY: SecretStr = ""
    AWS_REGION: str = "eu-central-1"

    S3_ENDPOINT_URL: str | None = None
    S3_BUCKET_NAME: str = "test-bucket"

    WEB_REQUEST_TIMEOUT: int = 10


@lru_cache
def get_app_config(filename: str = ".env") -> AppSettings:
    return AppSettings(_env_file=dotenv.find_dotenv(filename, usecwd=True))
