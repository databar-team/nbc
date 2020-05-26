from kasasa_common import get_mysql_connection, parse_db_envvars


def get_db_connection(context, **kwargs):
    db_dict = parse_db_envvars(secrets=context.VAULT_SECRETS,
                               **kwargs)
    return get_mysql_connection(**db_dict)