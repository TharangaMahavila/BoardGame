from database.db_init import init_database
from database.db_connection import get_connection, close_connection


def main():
    init_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    print("Users count:", cursor.fetchone()[0])

    cursor.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        close_connection()
