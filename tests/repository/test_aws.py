import os
import pytest
from unittest import mock

from boto3.exceptions import S3UploadFailedError
from testfixtures import TempDirectory

from src import exception


async def test_upload(aws_repo):
    with TempDirectory() as temp_dir:
        filename = "test.txt"
        temp_dir.write(filename, b'some thing')
        filepath = os.path.join(temp_dir.path, filename)

        await aws_repo.upload(filepath)

        assert True


async def test_upload_file_not_found(aws_repo):
    with pytest.raises(exception.FileError):
        await aws_repo.upload("/some_wrong_file")


async def test_upload_failed(aws_repo):
    client_mock = mock.MagicMock()
    client_mock.side_effect = S3UploadFailedError
    aws_repo.s3_client = client_mock
    with pytest.raises(exception.S3Error):
        await aws_repo.upload("/some_wrong_file")
