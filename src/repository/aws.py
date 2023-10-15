import os

from src import exception
from src.clients.aws import s3
from src.config import AppSettings


class Repository:
    def __init__(self, s3_client: s3.Client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    async def upload(self, filepath: str) -> None:
        try:
            await self.s3_client.upload(
                bucket=self.bucket_name,
                key=os.path.basename(filepath),
                filepath=filepath,
            )
        except (
            FileNotFoundError,
            EOFError,
        ):
            raise exception.FileError("Can't open file")
        except Exception:
            raise exception.S3Error("Uploading to s3 failed")


async def create(config: AppSettings) -> Repository:
    s3_client = await s3.create(config)
    return Repository(
        s3_client=s3_client,
        bucket_name=config.S3_BUCKET_NAME,
    )
