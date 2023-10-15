import os
import tempfile
import zipfile

from src.config import AppSettings
from src.exception import FileNotValid


class Repository:
    def __init__(self) -> None:
        pass

    def unpack_zip(self, filepath: str, dir_path: str) -> None:
        try:
            with zipfile.ZipFile(filepath, "r") as zip_ref:
                zip_ref.extractall(dir_path)
        except zipfile.BadZipfile:
            raise FileNotValid("Only .zip files allowed")

    def list_dir_files(
        self,
        dir_path: str,
    ) -> list[str]:
        result = []
        for file in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file)):
                result.append(file)

        return result

    def get_temp_dir(self) -> str:
        return tempfile.mkdtemp()

    def get_temp_file(self) -> str:
        _, filename = tempfile.mkstemp()
        return filename


def create(config: AppSettings) -> Repository:
    return Repository()
