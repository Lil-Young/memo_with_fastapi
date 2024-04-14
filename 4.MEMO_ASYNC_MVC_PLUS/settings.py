from pydantic import BaseSettings

class Settings(BaseSettings):
    mysql_uri: str

    class Config:
        env_file = ".env"

settings = Settings()
print(settings.mysql_uri)