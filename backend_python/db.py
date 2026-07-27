import os
import mysql.connector


def _get_env_value(key, default):
    value = os.environ.get(key)
    if value is None:
        return default
    value = str(value).strip()
    return value if value else default


def get_db_connection():
    return mysql.connector.connect(
        host=_get_env_value('DB_HOST', '127.0.0.1'),
        user=_get_env_value('DB_USER', 'root'),
        password=_get_env_value('DB_PASS', 'root'),
        database=_get_env_value('DB_NAME', 'helpreach_db'),
        port=int(_get_env_value('DB_PORT', '3306'))
    )
