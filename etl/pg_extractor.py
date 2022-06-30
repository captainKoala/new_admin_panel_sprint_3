import logging

import psycopg2
from psycopg2.extensions import connection


class PostgresExtractor:
    def __init__(self, conn: connection, logger: logging.Logger = None):
        self.conn = conn
        if logger is None:
            logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        self.logger = logger

    def get_movies(self):
        query = 'SELECT * FROM content.film_work;'
        cur = self.conn.cursor()
        res = cur.execute(query)
        self.logger.debug(res)
