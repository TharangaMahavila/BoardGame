import sys
import src.main.service.login_service as login


class LoginController:
    def __init__(self):
        self.user = None
        self.login_service = login.LoginService()

    def display_main_menu(self):
        menu_options = {
            "1": "User Login",
            "2": "New Member Registration",
            "q": "Exit"
            }

        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print()
                print("*"*50)
                print(f"***{"Welcome to the Online Boardgame Shop":^44}***")
                print("*"*50)

                for key, value in menu_options.items():
                    print(f"{key}) {value}")

                print()
                choice = input("Type in your choice:")
                print()
                if choice in menu_options.keys():
                    self._select_menu(choice)
                    if choice == "q":
                        break
                else:
                    raise ValueError()
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id):
        match menu_id:
            case "1":
                self._user_login()
            case "2":
                self._member_registration()
            case "q":
                self._exit()

    def _user_login(self):
        print()

    def _member_registration(self):
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print("== Welcome to the Online Boardgame Shop ==")
                print("== New Member Registration ==")
                first_name = input("Enter First Name:")
                last_name = input("Enter Last Name:")
                street = input("Enter Street:")
                city = input("Enter City:")
                postal_code = input("Enter Postal Code:")
                phone = input("Enter Phone (optional):")
                email = input("Enter Email address:")
                password = input("Enter Password:")
                print(self.login_service.member_registration(
                    first_name,
                    last_name,
                    street,
                    city,
                    postal_code,
                    phone,
                    email,
                    password
                ))
            except Exception as e:
                attempts += 1
                print(f"\nFailed to register member: {e}\n")
                choice = input("Would you like to re-enter (y/n):")
                if choice.lower() == "n":
                    self._exit()
                    break

    def _exit(self):
        print("Thank you for using Boardgame Shop!")
        sys.exit(0)
