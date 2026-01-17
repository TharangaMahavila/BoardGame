from src.main.util.route import Route


class MemberMenu:
    def __init__(self, context=None):
        # Store shared application context
        self.context = context

    def start(self):
        menu_options = {
            "1": "Browse by genre",
            "2": "Search by designer/title",
            "3": "View cart",
            "4": "Checkout",
            "5": "Log out"
            }

        attempts = 0    # Track invalid attempts
        while True:
            if attempts == 5:   # Limit attempts to 5
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print()
                print("*"*50)
                print(f"***{"Welcome to the Online Boardgame Shop":^44}***")
                print("*"*50)

                print("Member Menu:")
                for key, value in menu_options.items():
                    print(f"{key}) {value}")    # Display menu items

                print()
                choice = input("Type in your choice:")
                print()
                if choice in menu_options.keys():   # Validate user input
                    return self._select_menu(choice)    # Process selected option
                else:
                    raise ValueError()  # Invalid choice
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id):
        match menu_id:
            case "1":
                # Go to genre browsing
                return self._browse_by_genre()
            case "2":
                # Go to designer/title search
                return self._search_by_designer()
            case "3":
                # Go to cart
                return self._view_cart()
            case "4":
                # Go to checkout
                return self._checkout()
            case "5":
                # Log out
                return self._logout()

    def _browse_by_genre(self):
        # Navigate to genre screen
        return Route.GENRE

    def _search_by_designer(self):
        # Navigate to designer search
        return Route.DESIGNER

    def _view_cart(self):
        # Navigate to cart
        return Route.CART

    def _checkout(self):
        # Navigate to invoice
        return Route.INVOICE

    def _logout(self):
        # Clear logged-in user
        self.context.user = None
        # Return to login screen
        return Route.LOGIN
