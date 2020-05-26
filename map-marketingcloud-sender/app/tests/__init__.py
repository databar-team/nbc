# configuration for tests

import os
from os.path import join, dirname
from dotenv import load_dotenv
from kasasa_common import get_mysql_connection

from alembic.config import Config
from alembic import command


alembic_cfg = Config(join(dirname(__file__), "alembic.ini"))

def get_db_url():
    host = os.getenv('DATABASE_HOST')
    port = os.getenv('DATABASE_PORT')
    user = os.getenv('DATABASE_USERNAME')
    password = os.getenv('DATABASE_PASSWORD')
    schema = os.getenv('DATABASE_NAME')

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}"

def get_db_connection():
    return get_mysql_connection(database_url=get_db_url(), dict_cursor=True)

def run_db_migrations():
    command.upgrade(alembic_cfg, "head")

def teardown_db_migrations():
    command.downgrade(alembic_cfg, "base")