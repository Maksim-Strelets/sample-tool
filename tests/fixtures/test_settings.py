import pytest

from src import config


@pytest.fixture(scope="session")
def test_settings() -> config.AppSettings:
    return config.get_app_config(".env.test")
