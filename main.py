from database.db_init import init_database
from database.db_connection import close_connection
import src.main.controller.login_controller as login_controller


def main():
    init_database()
    login = login_controller.LoginController()
    login.display_main_menu()


if __name__ == "__main__":
    try:
        main()
    finally:
        close_connection()
