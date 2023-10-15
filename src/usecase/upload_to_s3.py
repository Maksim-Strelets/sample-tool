import asyncio
import os.path

from src.config import AppSettings
from src.repository import (
    aws,
    file,
    web,
)


class Usecase:
    def __init__(
        self,
        aws_repo: aws.Repository,
        file_repo: file.Repository,
        web_repo: web.Repository,
    ):
        self.aws_repo = aws_repo
        self.file_repo = file_repo
        self.web_repo = web_repo

    async def process(self, url: str) -> None:
        filepath = self.file_repo.get_temp_file()
        self.web_repo.download(url=url, filepath=filepath)
        dir_path = self.file_repo.get_temp_dir()
        self.file_repo.unpack_zip(filepath=filepath, dir_path=dir_path)
        await asyncio.gather(
            *[
                self.aws_repo.upload(os.path.join(dir_path, filename))
                for filename in self.file_repo.list_dir_files(dir_path)
            ]
        )


async def create(config: AppSettings) -> Usecase:
    aws_repo = await aws.create(config)
    file_repo = file.create(config)
    web_repo = web.create(config)
    return Usecase(
        aws_repo=aws_repo,
        file_repo=file_repo,
        web_repo=web_repo,
    )
