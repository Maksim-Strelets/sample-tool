import requests

from src.config import AppSettings
from src.exception import UrlNotValidException


class Repository:
    def __init__(self, timeout: int) -> None:
        self.timeout = timeout

    def download(self, url: str, filepath: str) -> None:
        try:
            response = requests.get(url, timeout=self.timeout)
            open(filepath, "wb").write(response.content)
        except requests.exceptions.RequestException:
            raise UrlNotValidException(f"Not valid url: {url}")


def create(config: AppSettings) -> Repository:
    return Repository(timeout=config.WEB_REQUEST_TIMEOUT)
