from src.main.util.route import Route
from src.main.repository.game_repository import GameRepository
from src.main.repository.cart_repository import CartRepository
from src.main.service.game_service import GameService
from src.main.service.cart_service import CartService


class DesignerController:
    def __init__(self, context=None):
        self.context = context
        self.game_repo = GameRepository()
        self.game_service = GameService(self.context, self.game_repo)
        self.cart_repo = CartRepository()
        self.cart_service = CartService(self.context, self.cart_repo, self.game_repo)

    def start(self):
        menu_options = {
            "1": "Search by designer (starts with)",
            "2": "Search by title (whole word)",
            "3": "Back"
        }

        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print("== Search ==")
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
                return self._search_by_starts_with()
            case "2":
                self._search_by_title()
            case "3":
                return self._back()

    def _search_by_starts_with(self):
        name = input("Designer starts with: ")
        page = 0
        page_size = 3
        total = self.game_service.get_designer_count(name)
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                start = page * page_size
                result = self.game_service.get_game_by_designer(name, page, page_size)
                print(f"== Results (showing {start+1}-{start+page_size} of {total})")
                if not result:
                    print("No more games.")
                    if page > 0:
                        page -= 1
                for item in result:
                    print(f"- ID {item["game_id"]}: {item["title"]} by {item["designer"]} ${item["unit_price"]}")
                print("Options: enter Game ID to add to cart, 'n' for next, ENTER to return")
                choice = input(">")
                if choice == "":
                    return
                elif choice.lower() == "n":
                    page += 1
                else:
                    qty = int(input("Quantity:"))
                    added = self.cart_service.save_to_cart(choice, qty)
                    print(added)
            except ValueError:
                attempts += 1
                print("Game Id or quantity is invalid. Please try again\n")

    def _search_by_title(self):
        name = input("Title word: ")
        page = 0
        page_size = 3
        total = self.game_service.get_title_count(name)
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                start = page * page_size
                result = self.game_service.get_game_by_title(name, page, page_size)
                print(f"== Results (showing {start+1}-{start+page_size} of {total})")
                if not result:
                    print("No more games.")
                    if page > 0:
                        page -= 1
                for item in result:
                    print(f"- ID {item["game_id"]}: {item["title"]} by {item["designer"]} ${item["unit_price"]}")
                print("Options: enter Game ID to add to cart, 'n' for next, ENTER to return")
                choice = input(">")
                if choice == "":
                    return
                elif choice.lower() == "n":
                    page += 1
                else:
                    qty = int(input("Quantity:"))
                    added = self.cart_service.save_to_cart(choice, qty)
                    print(added)
            except ValueError:
                attempts += 1
                print("Game Id or quantity is invalid. Please try again\n")

    def _back(self):
        return Route.MEMBER_MENU
