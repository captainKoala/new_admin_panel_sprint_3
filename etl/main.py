# docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0

import logging
import os
from functools import wraps
from pathlib import Path
from time import sleep

import requests
import psycopg2
from psycopg2.extras import RealDictCursor

from pg_extractor import PostgresExtractor
from settings import Settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


BASE_DIR = Path(__file__).resolve().parent

INDEX_NAME = 'movies'
ETL_BASE_URL = 'http://es'
ETL_PORT = '9200'

ETL_SCHEMA_FILE = MEDIA_ROOT = os.path.join(BASE_DIR, 'es_schema.json')


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time if start_sleep_time < border_sleep_time else border_sleep_time
            while True:
                try:
                    func(*args, **kwargs)
                    break
                except Exception as e:
                    logger.warning(f'An exception occurred. Next attempt in {sleep_time} seconds.\n{e}')
                    sleep(sleep_time)
                    sleep_time *= factor
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
        return inner

    return func_wrapper


@backoff()
def create_schema(url: str, name: str, schema: str):
    logger.debug('Create schema...')
    response = requests.put(url+name, data=schema, headers={'Content-Type': 'application/json'})
    logger.debug(response.json())

from data_helpers import FilmworkData
def es_update_movies(film_works: list[FilmworkData]) -> None:
    line_header = '{{"index": {{"_index": "{}", "_id": "{}"}}}}'


if __name__ == '__main__':
    with open(ETL_SCHEMA_FILE) as f:
        schema = f.read()

    dsl = {
        'dbname': Settings().postgres_db,
        'user': Settings().postgres_user,
        'password': Settings().postgres_password,
        'host': Settings().postgres_host,
        'port': Settings().postgres_port,
    }
    # create_schema(f'{ETL_BASE_URL}:{ETL_PORT}/', INDEX_NAME, schema)

    logger.debug('Connect to Postgres')
    with psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as pg_conn:
        pg_extractor = PostgresExtractor(pg_conn, logger)
        movies = pg_extractor.get_movies()

    counter = 1

    while True:
        logger.debug(f'{counter} ...')
        sleep(2)
        counter += 1
