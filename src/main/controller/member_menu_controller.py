from src.main.util.route import Route


class MemberMenu:
    def __init__(self, context=None):
        self.context = context

    def start(self):
        menu_options = {
            "1": "Browse by genre",
            "2": "Search by designer/title",
            "3": "View cart",
            "4": "Checkout",
            "5": "Log out"
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

                print("Member Menu:")
                for key, value in menu_options.items():
                    print(f"{key}) {value}")

                print()
                choice = input("Type in your choice:")
                print()
                if choice in menu_options.keys():
                    return self._select_menu(choice)
                else:
                    raise ValueError()
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id):
        match menu_id:
            case "1":
                return self._browse_by_genre()
            case "2":
                return self._search_by_designer()
            case "3":
                return self._view_cart()
            case "4":
                return self._checkout()
            case "5":
                return self._logout()

    def _browse_by_genre(self):
        return Route.GENRE

    def _search_by_designer(self):
        return Route.DESIGNER

    def _view_cart(self):
        return Route.CART

    def _checkout(self):
        return Route.INVOICE

    def _logout(self):
        self.context.user = None
        return Route.LOGIN
