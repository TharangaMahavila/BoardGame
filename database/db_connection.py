import mysql.connector
from config import DB_CONFIG

_connection = None


def get_connection():
    try:
        global _connection

        # If no connection exists OR the connection is closed, create a new one
        if _connection is None or not _connection.is_connected():
            _connection = mysql.connector.connect(**DB_CONFIG)

        # Return the active connection
        return _connection
    except Exception:
        print("Failed to initialize database connection")


def close_connection():
    global _connection
    # If a connection exists and is still open, close it
    if _connection and _connection.is_connected():
        # Close the database connection
        _connection.close()
        # Reset connection variable
        _connection = None
