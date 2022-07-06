import requests

from data_helpers import FilmworkData
from logger import logger
from utils import backoff

# ToDo: use settings!!!
INDEX_NAME = 'movies'


@backoff(no_raise_exceptions=[Exception])
def create_schema(url: str, name: str, schema: str) -> None:
    logger.debug('Create schema...')
    response = requests.put(url+name, data=schema, headers={'Content-Type': 'application/json'})
    logger.debug(response.json())


def es_update_records(url: str, schema_name: str, film_works: list[FilmworkData]) -> None:
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