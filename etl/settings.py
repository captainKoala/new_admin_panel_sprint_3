from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = 'db'
    postgres_port: str = '5432'
    es_host: str = 'es'
    es_port: str = '9200'
    es_index_name: str = 'movies'
    logger_name: str = 'etl_service'
    query_batch_size: int = 100
    update_checking_frequency_sec: int = 10

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
