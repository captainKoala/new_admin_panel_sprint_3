import os
from pathlib import Path
from datetime import datetime, timezone
from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor

from elasticsearch import create_schema, es_update_records
from logger import logger
from postgres_connector import get_modified_film_works
from settings import Settings
from state import JsonFileStorage, State


BASE_DIR = Path(__file__).resolve().parent


# ToDo: use import from settings and .env!!!
INDEX_NAME = 'movies'
ETL_BASE_URL = 'http://es'
ETL_PORT = '9200'

ETL_SCHEMA_FILE = os.path.join(BASE_DIR, 'es_schema.json')
STATE_FILE = '/data/state.txt'
QUERY_BATCH_SIZE = 100
INITIAL_CHECKED_DATETIME = datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
UPDATE_CHECKING_FREQUENCY_SEC = 10

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

    while True:
        logger.debug('Connect to Postgres DB')
        with psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as pg_conn:
            last_checked = state.get_state('movies_create_last_checked_date')
            if not last_checked:
                last_checked = INITIAL_CHECKED_DATETIME

            current_time = datetime.now()
            limit = QUERY_BATCH_SIZE
            offset = 0
            while True:
                logger.debug('Get new data batch')
                new_film_works = get_modified_film_works(conn=pg_conn,
                                                         last_date=last_checked,
                                                         limit=limit,
                                                         offset=offset)
                if not new_film_works:
                    logger.debug('No data to update')
                    break
                logger.debug('Update ElasticSearch index')
                es_update_records(f'{ETL_BASE_URL}:{ETL_PORT}/', INDEX_NAME, new_film_works)
                offset += QUERY_BATCH_SIZE
        sleep(UPDATE_CHECKING_FREQUENCY_SEC)
