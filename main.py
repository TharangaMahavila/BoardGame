from database.db_init import init_database
from database.db_connection import close_connection
from src.main.controller.router_controller import RouterController


def main():
    init_database()
    router = RouterController()
    router.start()


if __name__ == "__main__":
    try:
        main()
    finally:
        close_connection()
