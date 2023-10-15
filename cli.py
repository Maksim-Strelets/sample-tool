import asyncio

import fire

from src.config import get_app_config
from src.usecase import upload_to_s3
from src.exception import BaseError


def upload_to_s3_script(url: str) -> None:
    async def _upload_to_s3_script() -> None:
        try:
            config = get_app_config()
            usecase = await upload_to_s3.create(config)
            await usecase.process(url)
            print("Uploading done")
        except BaseError as e:
            print("Something went wrong:", e)

    asyncio.run(_upload_to_s3_script())


if __name__ == '__main__':
    fire.Fire({
        "upload_to_s3_script": upload_to_s3_script,
    })
