import os
from pathlib import Path
from datetime import datetime, timezone
from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor

from elasticsearch import create_index, es_update_records
from logger import logger
from postgres_connector import get_modified_film_works
from settings import Settings
from state import JsonFileStorage, State


BASE_DIR = Path(__file__).resolve().parent


ETL_SCHEMA_FILE = os.path.join(BASE_DIR, 'es_schema.json')
STATE_FILE = '/data/state.txt'

ES_URL = f'http://{Settings().es_host}:{Settings().es_port}/'
QUERY_BATCH_SIZE = Settings().query_batch_size
UPDATE_CHECKING_FREQUENCY_SEC = Settings().update_checking_frequency_sec
INITIAL_CHECKED_DATETIME = datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

POSTGRES_DSL = {
    'dbname': Settings().postgres_db,
    'user': Settings().postgres_user,
    'password': Settings().postgres_password,
    'host': Settings().postgres_host,
    'port': Settings().postgres_port,
}


if __name__ == '__main__':
    index_name = Settings.es_index_name
    state = State(JsonFileStorage(STATE_FILE))

    if not state.is_state('is_index_created', 1):
        with open(ETL_SCHEMA_FILE) as f:
            schema = f.read()
        create_index(ES_URL, index_name, schema)
        state.set_state('is_index_created', 1)

    while True:
        logger.debug('Connect to Postgres DB')
        with psycopg2.connect(**POSTGRES_DSL, cursor_factory=RealDictCursor) as pg_conn:
            last_checked = state.get_state('movies_create_last_checked_date')
            if not last_checked:
                last_checked = INITIAL_CHECKED_DATETIME
            logger.debug(f'Last checked: {last_checked}')

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
                logger.debug(f'{len(new_film_works)} records need to be updated')

                es_update_records(ES_URL, index_name, new_film_works)
                offset += QUERY_BATCH_SIZE
            state.set_state('movies_create_last_checked_date', current_time)

        logger.debug(f'Next check in {UPDATE_CHECKING_FREQUENCY_SEC} seconds\n')
        sleep(UPDATE_CHECKING_FREQUENCY_SEC)
