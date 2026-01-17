import getpass
from src.main.service.login_service import LoginService
from src.main.repository.user_repository import UserRepository
from src.main.util.route import Route


class LoginController:
    def __init__(self, context=None):
        # Shared application context
        self.context = context
        # Create user repository
        self.user_repo = UserRepository()
        # Create login service
        self.login_service = LoginService(self.context, self.user_repo)

    def start(self):
        menu_options = {
            "1": "User Login",
            "2": "New Member Registration",
            "q": "Exit"
            }

        attempts = 0    # Track invalid attempts
        while not self.context.user:    # Loop until user is logged in
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print()
                print("*"*50)
                print(f"***{"Welcome to the Online Boardgame Shop":^44}***")
                print("*"*50)

                for key, value in menu_options.items():
                    print(f"{key}) {value}")    # Display menu options

                print()
                choice = input("Type in your choice:")
                print()
                if choice in menu_options.keys():   # Validate input
                    return self._select_menu(choice)    # Process selection
                else:
                    raise ValueError()  # Invalid choice
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id):
        match menu_id:
            case "1":
                return self._user_login()   # Go to login flow
            case "2":
                self._member_registration()  # Go to registration flow
            case "q":
                return self._exit()  # Exit application

    def _user_login(self):
        attempts = 0    # Track login attempts
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print("== Welcome to the Online Boardgame Shop ==")
                print("== User Login ==")
                email = input("Enter Email:")   # Get email from user
                password = getpass.getpass("Enter Password:")   # Get password securely
                # Validate credentials
                user = self.login_service.user_login(email, password)
                if user:
                    print("Login Successful.")
                    self.context.user = user    # Store logged-in user in context
                    return Route.MEMBER_MENU    # Go to member menu
            except Exception as e:
                attempts += 1
                print(f"\nFailed to login: {e}\n")
                choice = input("Would you like to re-enter (y/n):")
                if choice.lower() == "n":
                    self._exit()    # Exit if user chooses not to retry
                    break

    def _member_registration(self):
        attempts = 0    # Track registration attempts
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

                # Register new user
                new_member = self.login_service.member_registration(
                    first_name,
                    last_name,
                    street,
                    city,
                    postal_code,
                    phone,
                    email,
                    password
                )

                if new_member:
                    print("\nRegistration successful, Please login from main menu")
                    break
            except Exception as e:
                attempts += 1
                print(f"\nFailed to register member: {e}\n")
                choice = input("Would you like to re-enter (y/n):")
                if choice.lower() == "n":
                    self._exit()    # Exit if user cancels
                    break

    def _exit(self):
        # Return exit route
        return Route.EXIT
