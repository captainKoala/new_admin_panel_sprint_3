from datetime import datetime
import logging

from psycopg2.extensions import connection

from data_helpers import FilmworkData
from logger import logger
from utils import backoff


class PostgresExtractor:
    def __init__(self, conn: connection, custom_logger: logging.Logger = None):
        self.conn = conn
        self.logger = custom_logger if custom_logger else logger

    @backoff()
    def get_modified_film_works(self, last_date: datetime, limit: int = 100, offset: int = 0):
        logger.debug(f'limit={limit}, offset={offset}')
        query = '''
                SELECT fw.id, fw.title, fw.description, fw.rating, fw.type, fw.created, fw.modified,
                   COALESCE (
                       json_agg(
                           DISTINCT jsonb_build_object(
                               'person_role', pfw.role,
                               'person_id', p.id,
                               'person_name', p.full_name
                           )
                       ) FILTER (WHERE p.id is not null),
                       '[]'
                   ) as persons,
                   array_agg(DISTINCT g.name) as genres
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.modified > %s
                GROUP BY fw.id
                ORDER BY fw.modified
                LIMIT %s
                OFFSET %s;
                '''
        cur = self.conn.cursor()
        cur.execute(query, (last_date, limit, offset))
        res = cur.fetchall()
        films = [FilmworkData(**f) for f in res]
        return films



