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
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        port=int(os.environ.get('DB_PORT', 3306))
    )
