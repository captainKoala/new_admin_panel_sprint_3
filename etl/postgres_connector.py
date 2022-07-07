from datetime import datetime

from psycopg2.extensions import connection

from data_helpers import FilmworkData
from utils import backoff


def _get_query_modified_film_works() -> str:
    """Returns a query to get data to update the ElasticSearch index (film work, genre or person update."""
    return '''
        SELECT
           fw.id,
           fw.title,
           fw.description,
           fw.rating,
           fw.type,
           fw.created,
           fw.modified,
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
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        WHERE fw.modified > %s OR g.modified > %s OR p.modified > %s
        GROUP BY fw.id
        ORDER BY fw.modified
        LIMIT %s OFFSET %s;
        '''


@backoff(no_raise_exceptions=[Exception])
def get_modified_film_works(conn: connection, last_date: datetime, limit: int = 100, offset: int = 0) -> list[FilmworkData]:
    """
    Returns the data that should be updated in the ElasticSearch index.

    :param conn: psycopg2 connection
    :param last_date: the date after which the data update should be checked
    :param limit: the LIMIT SQL-parameter
    :param offset: the OFFSET SQL-parameter
    :returns films: the list of FilmWorkData
    """
    query = _get_query_modified_film_works()
    cur = conn.cursor()
    cur.execute(query, (last_date, last_date, last_date, limit, offset))
    res = cur.fetchall()
    films = [FilmworkData(**f) for f in res]
    return films
