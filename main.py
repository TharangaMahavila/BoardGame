from database.db_init import init_database
from database.db_connection import close_connection, fetchone


def main():
    init_database()

    print(fetchone("SELECT COUNT(*) FROM users"))


if __name__ == "__main__":
    try:
        main()
    finally:
        close_connection()
