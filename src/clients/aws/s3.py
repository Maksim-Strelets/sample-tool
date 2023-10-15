import aioboto3

from src.config import AppSettings


class Client:
    def __init__(
        self,
        aws_session: aioboto3.Session,
        aws_endpoint_url: str | None,
    ):
        self._session = aws_session
        self.aws_endpoint_url = aws_endpoint_url

    async def upload(self, bucket: str, key: str, filepath: str) -> None:
        async with self._session.client(
            "s3",
            endpoint_url=self.aws_endpoint_url,
        ) as s3_client:
            await s3_client.upload_file(filepath, bucket, key)


async def create(config: AppSettings) -> Client:
    session = aioboto3.Session(
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_KEY,
        aws_secret_access_key=config.AWS_SECRET_KEY.get_secret_value(),
    )

    return Client(
        aws_session=session,
        aws_endpoint_url=config.S3_ENDPOINT_URL,
    )
