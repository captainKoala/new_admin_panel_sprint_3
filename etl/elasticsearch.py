import requests

from data_helpers import FilmworkData
from logger import logger
from utils import backoff


@backoff(no_raise_exceptions=[Exception])
def create_index(url: str, name: str, schema: str) -> None:
    """
    Create ElasticSearch index.

    :param url: URL to connect to ES, like 'http://127.0.0.1:9200/'
    :param name: index name
    :param schema: index schema
    :return: None
    """
    logger.debug('Create index...')
    if not url.endswith('/'):
        url += '/'
    response = requests.put(f'{url}{name}/', data=schema, headers={'Content-Type': 'application/json'})
    logger.debug(response.json())


def es_update_records(url: str, index_name: str, film_works: list[FilmworkData]) -> None:
    """
    Update Film Work data in ElasticSearch index.

    :param url: URL to connect to ES, like 'http://127.0.0.1:9200/'
    :param index_name: index name
    :param film_works: data to update
    :return: None
    """
    logger.debug('Update ElasticSearch index')
    if not url.endswith('/'):
        url += '/'
    query_data = ''
    line_header = '{{"index": {{"_index": "{}", "_id": "{}"}}}}\n'
    for fw in film_works:
        odd = line_header.format(index_name, fw.id)
        even = fw.json(exclude={'persons': True, 'actors': {'__all__': {'person_role'}}})
        query_data += f'{odd}{even}\n'
    requests.post(
        url=f'{url}{index_name}/_bulk?filter_path=items.*.error',
        data=query_data,
        headers={'Content-Type': 'application/x-ndjson'},
    )
