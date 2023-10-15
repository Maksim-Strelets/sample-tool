from os import path
import pytest
from unittest import mock
from testfixtures import TempDirectory

from src import exception


def test_temp_file(file_repo):
    _path = file_repo.get_temp_file()

    assert path.isfile(_path)


def test_temp_dir(file_repo):
    _path = file_repo.get_temp_dir()

    assert path.isdir(_path)


def test_list_dir_files(file_repo):
    with TempDirectory() as temp_dir:
        filenames = ["test{}.txt".format(i) for i in range(5)]
        for filename in filenames:
            temp_dir.write(filename, b'some thing')

        result = file_repo.list_dir_files(temp_dir.path)

        assert set(filenames) == set(result)


def test_list_dir_files_skip_dirs(file_repo):
    with TempDirectory() as temp_dir:
        filenames = ["test{}.txt".format(i) for i in range(5)]
        for filename in filenames:
            temp_dir.write(filename, b'some thing')
        temp_dir.makedir(path.join(temp_dir.path, "test_dir"))

        result = file_repo.list_dir_files(temp_dir.path)

        assert set(filenames) == set(result)


def test_unpack_zip(file_repo):
    filepath = "test_file"
    dir_path = "test_dir"

    with mock.patch("zipfile.ZipFile") as zipfile_mock:
        file_repo.unpack_zip(filepath=filepath, dir_path=dir_path)

    for call in [
        mock.call(filepath, "r"),
        mock.call().__enter__().extractall(dir_path),
    ]:
        assert call in zipfile_mock.mock_calls


def test_unpack_wrong_file(file_repo):
    with TempDirectory() as temp_dir:
        filename = "test.txt"
        temp_dir.write(filename, b'some thing')

        with pytest.raises(exception.FileNotValid):
            file_repo.unpack_zip(
                filepath=path.join(temp_dir.path, filename),
                dir_path=temp_dir.path
            )
