import os
from os.path import join, dirname
from dotenv import load_dotenv
from config.context import build_context
from kasasa_common.database import get_connection_object
from pathlib import Path

from alembic.config import Config
from alembic import command

alembic_cfg = Config(join(dirname(__file__), "alembic.ini"))

def get_db_connection():
    restore_os_env()
    context = build_context('worker')
    return get_connection_object(context.WRITER_CONTEXT)


def run_db_migrations():
    command.upgrade(alembic_cfg, "head")


def teardown_db_migrations():
    command.downgrade(alembic_cfg, "base")


def restore_os_env():
    env_path = './tests/.env.test'
    load_dotenv(dotenv_path=env_path)