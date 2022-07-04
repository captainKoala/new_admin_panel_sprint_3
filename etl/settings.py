from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    logger_name: str = 'etl_service'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
