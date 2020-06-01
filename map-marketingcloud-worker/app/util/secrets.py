import os

from kasasa_common.context import VaultContext
from kasasa_common.vault import get_vault_secrets


def get_secrets(logger, local_secrets=None, secrets_f=get_vault_secrets, **_kwargs):
    logger.debug('Getting secrets')
    if os.getenv('SKIP_VAULT'):
        return get_local_secrets(logger, local_secrets=local_secrets)
    else:
        return get_remote_secrets(logger, secrets_f=secrets_f)


def get_remote_secrets(logger, secrets_f=get_vault_secrets):
    logger.debug('Getting remote secrets')
    vault_config = {
        'VAULT_ADDRESS': os.getenv('VAULT_ADDRESS'),
        'VAULT_APPROLE_PATH': os.getenv('VAULT_APPROLE_PATH'),
        'VAULT_APPROLE_SECRET_ID': os.getenv('VAULT_APPROLE_SECRET_ID'),
        'VAULT_SECRET_KEY': os.getenv('VAULT_SECRET_KEY')
    }
    context = VaultContext(**vault_config)
    return secrets_f(context=context)


def get_local_secrets(logger, local_secrets=None):
    logger.debug('Getting local secrets')
    secrets = dict(
        DATABASE_HOST=os.getenv('DATABASE_HOST', None),
        DATABASE_PORT=os.getenv('DATABASE_PORT', 3306),
        DATABASE_USERNAME=os.getenv('DATABASE_USERNAME', None),
        DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD', None),
    )
    secrets[os.getenv('DATABASE_PASSWORD_KEY')] = secrets.get('DATABASE_PASSWORD', '')
    if local_secrets:
        secrets.update(local_secrets)
    return secrets
