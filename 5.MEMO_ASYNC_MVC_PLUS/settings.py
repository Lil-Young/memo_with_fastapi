import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Settings(BaseSettings):
    mysql_url: str
    secret_key: str
    test_env: str = "test value입니다."

    model_config = SettingsConfigDict(
        env_file=BASE_DIR + '/.env',
        env_file_encoding='utf-8',
    )