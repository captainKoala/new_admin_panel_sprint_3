from datetime import datetime, timezone
import logging

from psycopg2.extensions import connection

from data_helpers import FilmworkData


class PostgresExtractor:
    def __init__(self, conn: connection, logger: logging.Logger = None):
        self.conn = conn
        if logger is None:
            logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        self.logger = logger

    def get_query(self, date_field: str = 'modified'):
        query = f'''
                SELECT fw.id, fw.title, fw.description, fw.rating, fw.type, fw.{ date_field },
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
                WHERE fw.{ date_field } > %s
                GROUP BY fw.id
                ORDER BY fw.{ date_field }
                LIMIT %s;
                '''
        return query

    def get_new_film_works(self, last_date: datetime = datetime(2000, 6, 16, 20, 14, 9, 222292, tzinfo=timezone.utc),
                           limit: int = 100):
        query = self.get_query('created')

        cur = self.conn.cursor()
        cur.execute(query, (last_date, limit))

        res = cur.fetchall()

        self.logger.debug(res)

        films = [FilmworkData(**f) for f in res]
        return films



