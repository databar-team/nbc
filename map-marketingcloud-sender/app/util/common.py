import os
import re

from config import SQL_PATH
from util.logger import logger


non_word_chars = re.compile(r'[^a-zA-Z0-9_]')


def get_context_vars(**kwargs):
    if kwargs.get('context_vars', None):
        return kwargs.get('context_vars')
    from config.context import get_env_vars
    return get_env_vars()


def get_secrets(secrets=None, **kwargs):
    logger.debug('getting secrets')

    if secrets:
        if os.getenv('SKIP_VAULT'):
            secrets[os.getenv('DATABASE_PASSWORD_KEY')] = os.getenv('DATABASE_PASSWORD')
        return secrets

    from interface.vault import vault_secrets
    return vault_secrets()


def get_sql(sql_file_name, replacement_values=dict()):
    with open(os.path.join(SQL_PATH, sql_file_name)) as sql_file:
        sql = sql_file.read()
    if replacement_values:
        sql = sql.format(**replacement_values)
    return sql


def generate_sql_insert_values(data, known_fields):
    """
    takes valid (known) fields and creates formatting values to be replaced by sql later
    e.g.: turns data = {'field_name1': 'some value', 'field_name2': 'some other value', ...}
          into string: '%(field_name1)s, %(field_name2)s, ...'
    """
    output = []
    for i, record in enumerate(data):
        full_values = []
        for field in known_fields:
            full_values.append("".join(["%(", str(i), field, ")s"]))
        output.append(''.join(["(", ', '.join(full_values), ")"]))
    return ', '.join(output)


def flatten_dict_for_sql_insert_replaces(data, known_fields):
    # flatten the records into a single dict so that all the values are at the fore
    replace_data = dict()
    for i, record in enumerate(data):
        for field in known_fields:
            replace_data[f'{i}{field}'] = record.get(field)

    return replace_data


def clean_user_sql_input(_input):
    if type(_input) != str:
        return ''

    cleaned = re.sub(non_word_chars, '', _input)
    return cleaned