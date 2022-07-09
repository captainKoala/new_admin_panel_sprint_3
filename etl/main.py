from datetime import datetime
from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor

from elasticsearch import create_index, es_update_records
from logger import logger
from postgres_connector import get_modified_film_works
from settings import Settings
from state import JsonFileStorage, State


STATE_FILE = '/data/state.txt'


if __name__ == '__main__':
    index_name = Settings().es_index_name
    state = State(JsonFileStorage(STATE_FILE))

    if not state.is_state('is_index_created', 1):
        with open(Settings().es_schema_file) as f:
            schema = f.read()
        create_index(Settings().es_url, index_name, schema)
        state.set_state('is_index_created', 1)

    while True:
        logger.debug('Connect to Postgres DB')
        dsl = {
            'dbname': Settings().postgres_db,
            'user': Settings().postgres_user,
            'password': Settings().postgres_password,
            'host': Settings().postgres_host,
            'port': Settings().postgres_port,
        }
        with psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as pg_conn:
            last_checked = state.get_state('movies_create_last_checked_date')
            if not last_checked:
                last_checked = datetime.min
            logger.debug(f'Last checked: {last_checked}')

            current_time = datetime.now()
            limit = Settings().query_batch_size
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

                es_update_records(Settings().es_url, index_name, new_film_works)
                offset += Settings().query_batch_size
            state.set_state('movies_create_last_checked_date', current_time)

        logger.debug(f'Next check in {Settings().update_checking_frequency_sec} seconds\n')
        sleep(Settings().update_checking_frequency_sec)
