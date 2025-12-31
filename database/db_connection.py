import mysql.connector
from config import DB_CONFIG

_connection = None


def get_connection():
    try:
        global _connection

        if _connection is None or not _connection.is_connected():
            _connection = mysql.connector.connect(**DB_CONFIG)

        return _connection
    except Exception:
        print("Failed to initialize database connection")


def close_connection():
    global _connection
    if _connection and _connection.is_connected():
        _connection.close()
        _connection = None


def fetchone(query):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    finally:
        cursor.close()
