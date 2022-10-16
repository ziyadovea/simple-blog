from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

DB_USERNAME = environ.get('DB_USERNAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
