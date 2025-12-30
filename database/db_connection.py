import mysql.connector
from config import DB_CONFIG

_connection = None


def get_connection():
    global _connection

    if _connection is None or not _connection.is_connected():
        _connection = mysql.connector.connect(**DB_CONFIG)

    return _connection


def close_connection():
    global _connection
    if _connection and _connection.is_connected():
        _connection.close()
        _connection = None
