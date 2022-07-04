import logging

from settings import Settings


logger = logging.getLogger(Settings().logger_name)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
