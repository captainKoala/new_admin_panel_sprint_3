# docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0

import os
from pathlib import Path
from datetime import datetime, timezone
from time import sleep

import requests
import psycopg2
from psycopg2.extras import RealDictCursor

from data_helpers import FilmworkData
from logger import logger
from pg_extractor import PostgresExtractor
from settings import Settings
from state import JsonFileStorage, State
from utils import backoff


BASE_DIR = Path(__file__).resolve().parent

INDEX_NAME = 'movies'
ETL_BASE_URL = 'http://es'
ETL_PORT = '9200'

ETL_SCHEMA_FILE = os.path.join(BASE_DIR, 'es_schema.json')
STATE_FILE = '/data/state.txt'
BATCH_SIZE = 100


@backoff()
def create_schema(url: str, name: str, schema: str):
    logger.debug('Create schema...')
    response = requests.put(url+name, data=schema, headers={'Content-Type': 'application/json'})
    logger.debug(response.json())


def es_create_movies(url: str, schema_name: str, film_works: list[FilmworkData]) -> None:
    query_data = ''
    line_header = '{{"index": {{"_index": "{}", "_id": "{}"}}}}\n'
    for fw in film_works:
        odd = line_header.format(INDEX_NAME, fw.id)
        even = fw.json(exclude={'id': True, 'genres': True, 'persons': True, 'actors': {'__all__': {'person_role'}}},
                       by_alias=True)
        query_data += f'{odd}{even}\n'
    response = requests.post(
        url=f'{url}{schema_name}/_bulk?filter_path=items.*.error',
        data=query_data,
        headers={'Content-Type': 'application/x-ndjson'},
    )
    logger.info(response.json())


if __name__ == '__main__':

    state = State(JsonFileStorage(STATE_FILE))

    if not state.is_state('is_index_created', 1):
        with open(ETL_SCHEMA_FILE) as f:
            schema = f.read()
        create_schema(f'{ETL_BASE_URL}:{ETL_PORT}/', INDEX_NAME, schema)
        state.set_state('is_index_created', 1)

    dsl = {
        'dbname': Settings().postgres_db,
        'user': Settings().postgres_user,
        'password': Settings().postgres_password,
        'host': Settings().postgres_host,
        'port': Settings().postgres_port,
    }

    logger.debug('Connect to Postgres')
    with psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as pg_conn:
        pg_extractor = PostgresExtractor(pg_conn)

        last_checked = state.get_state('movies_create_last_checked_date')
        if not last_checked:
            last_checked = datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

        current_time = datetime.now()
        limit = BATCH_SIZE
        offset = 0
        while True:
            new_film_works = pg_extractor.get_modified_film_works(last_date=last_checked, limit=limit, offset=offset)
            if not new_film_works:
                break
            es_create_movies(f'{ETL_BASE_URL}:{ETL_PORT}/', INDEX_NAME, new_film_works)
            offset += BATCH_SIZE

        # state.set_state('movies_create_last_checked_date', current_time)

        # es_update_movies(f'{ETL_BASE_URL}:{ETL_PORT}/', INDEX_NAME, movies)

    while True:
        logger.debug(datetime.now())
        sleep(5)
