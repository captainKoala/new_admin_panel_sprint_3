# docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0

import logging
import os
from pathlib import Path
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


BASE_DIR = Path(__file__).resolve().parent

INDEX_NAME = 'table'
ETL_BASE_URL = 'http://127.0.0.1'
ETL_PORT = '9200'

ETL_SCHEMA_FILE = MEDIA_ROOT = os.path.join(BASE_DIR, 'es_schema.json')


def create_schema(url: str, name: str, schema: str):
    response = requests.put(url+name, data=schema, headers={'Content-Type': 'application/json'})
    from pprint import pprint
    pprint(response.json())


if __name__ == '__main__':
    with open('test.json') as f:
        schema = f.read()
    create_schema(f'{ETL_BASE_URL}:{ETL_PORT}/', INDEX_NAME, schema)
