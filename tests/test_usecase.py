import os.path
from unittest import mock

from src.usecase import upload_to_s3


async def test_process():
    test_url = "https://test.com/archive.zip"
    zipped_files = ["1.txt", "2.jpg", "3.mov"]
    filename = "archive.zip"
    dir_path = "/tmp/dir"
    filepath = os.path.join(dir_path, filename)

    aws_repo = mock.AsyncMock()

    file_repo = mock.MagicMock()
    file_repo.get_temp_file.return_value = filepath
    file_repo.get_temp_dir.return_value = dir_path
    file_repo.list_dir_files.return_value = zipped_files

    web_repo = mock.MagicMock()

    usecase = upload_to_s3.Usecase(
        aws_repo=aws_repo,
        file_repo=file_repo,
        web_repo=web_repo,
    )

    await usecase.process(test_url)

    web_repo.download.assert_called_once_with(url=test_url, filepath=filepath)
    file_repo.unpack_zip.assert_called_once_with(
        filepath=filepath, dir_path=dir_path,
    )
    aws_repo.upload.assert_has_awaits(
        [mock.call(os.path.join(dir_path, file)) for file in zipped_files]
    )
