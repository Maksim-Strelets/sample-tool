import pytest
import requests

from src import exception


def test_download(web_repo, requests_mock):
    test_url = "http://test.com"
    filepath = "test.txt"
    content = b"test"
    requests_mock.get(test_url, content=content)

    web_repo.download(url=test_url, filepath=filepath)

    with open(filepath, "rb") as file:
        assert content == file.read()


def test_download_timeout(web_repo, requests_mock):
    test_url = "http://test.com"
    filepath = "test.txt"
    requests_mock.get(test_url, exc=requests.exceptions.ConnectTimeout)

    with pytest.raises(exception.UrlNotValidException):
        web_repo.download(url=test_url, filepath=filepath)


def test_download_not_found(web_repo, requests_mock):
    test_url = "http://test.com"
    filepath = "test.txt"
    requests_mock.get(test_url, exc=requests.exceptions.ConnectionError)

    with pytest.raises(exception.UrlNotValidException):
        web_repo.download(url=test_url, filepath=filepath)


def test_download_wrong_url(web_repo, requests_mock):
    test_url = "test"
    filepath = "test.txt"
    requests_mock.get(test_url, exc=requests.exceptions.MissingSchema)

    with pytest.raises(exception.UrlNotValidException):
        web_repo.download(url=test_url, filepath=filepath)