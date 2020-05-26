import os
from pathlib import Path
from dotenv import load_dotenv
from kasasa_common import get_vault_secrets
from util.logger import logger
from util.common import clean_user_sql_input

__context = None

class Context:
    def __init__(self, **kwargs):
        self.DATABASE_HOST = kwargs.get('DATABASE_HOST', None)
        self.DATABASE_PORT = kwargs.get('DATABASE_PORT', None)
        self.DATABASE_NAME = kwargs.get('DATABASE_NAME', None)
        self.DATABASE_USERNAME = kwargs.get('DATABASE_USERNAME', None)
        self.DATABASE_PASSWORD = kwargs.get('DATABASE_PASSWORD', None)
        self.DATABASE_PASSWORD_KEY = kwargs.get('DATABASE_PASSWORD_KEY', None)

        if os.getenv('SKIP_VAULT'):
            self.VAULT_SECRETS = {
                os.getenv('DATABASE_PASSWORD_KEY', 'dbpwk'): os.getenv('DATABASE_PASSWORD', ''),
                os.getenv('MC_AUTH_SECRET_KEY', "mcauthkey"): os.getenv('MC_AUTH_SECRET', '')
            }
        else:
            self.VAULT_SECRETS = get_vault_secrets(logger=logger)

        self.VAULT_ADDRESS = kwargs.get('VAULT_ADDRESS', None)
        self.VAULT_APPROLE_SECRET_ID = kwargs.get('VAULT_APPROLE_SECRET_ID', None)
        self.VAULT_APPROLE_PATH = kwargs.get('VAULT_APPROLE_PATH', None)
        self.VAULT_SECRET_KEY = kwargs.get('VAULT_SECRET_KEY', None)
        self.ENV = kwargs.get('ENV', None)

        self.MC_AUTH_URL = kwargs.get('MC_AUTH_URL', None)
        self.MC_AUTH_ID = kwargs.get('MC_AUTH_ID', None)
        self.MC_AUTH_SECRET_KEY = kwargs.get('MC_AUTH_SECRET_KEY', None)
        self.MC_AUTH_SECRET = self.VAULT_SECRETS.get(self.MC_AUTH_SECRET_KEY)
        self.MC_REST_URL = kwargs.get('MC_REST_URL', None)
        self.API_BATCH_SIZE = kwargs.get('API_BATCH_SIZE', 50)


def get_env_vars():
    if os.getenv('SKIP_VAULT'):
        env_path = Path('.') / '.env.local' or Path('.') / '.env.test'
    else:
        env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    return os.environ

def set_context():
    global __context

    env = get_env_vars()

    __context = Context(**env)

def get_context():
    if not __context:
        raise RuntimeError("Context not set.")

    return __context