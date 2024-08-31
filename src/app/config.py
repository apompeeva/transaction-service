import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST_POMPEEVA')
DB_PORT = os.environ.get('DB_PORT_POMPEEVA')
DB_NAME = os.environ.get('DB_NAME_POMPEEVA')
DB_USER = os.environ.get('DB_USER_POMPEEVA')
DB_PASS = os.environ.get('DB_PASS_POMPEEVA')
