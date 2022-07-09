import os
from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = 'db'
    postgres_port: str = '5432'
    es_host: str = 'es'
    es_port: str = '9200'
    es_url: str | None
    es_index_name: str = 'movies'
    es_schema_file: str = 'es_schema.json'
    logger_name: str = 'etl_service'
    query_batch_size: int = 100
    update_checking_frequency_sec: int = 1

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @root_validator
    def compute_es_url(cls, values):
        es_host = values.get('es_host')
        es_port = values.get('es_port')
        values['es_url'] = f'http://{es_host}:{es_port}/'
        return values
