import os


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

INTERNAL_IPS = os.environ.get('INTERNAL_IPS', '127.0.0.1,localhost').split(',')
