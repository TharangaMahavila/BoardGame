from src.main.util.route import Route
from src.main.repository.game_repository import GameRepository
from src.main.repository.cart_repository import CartRepository
from src.main.service.game_service import GameService
from src.main.service.cart_service import CartService


class DesignerController:
    def __init__(self, context=None):
        self.context = context
        self.game_repo = GameRepository()
        # Create game service
        self.game_service = GameService(self.context, self.game_repo)
        self.cart_repo = CartRepository()
        # Create cart service
        self.cart_service = CartService(self.context, self.cart_repo, self.game_repo)

    def start(self):
        menu_options = {
            "1": "Search by designer (starts with)",
            "2": "Search by title (whole word)",
            "3": "Back"
        }

        attempts = 0    # Count invalid attempts
        while True:
            if attempts == 5:   # Limit user to 5 invalid inputs
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print("== Search ==")
                for key, value in menu_options.items():
                    print(f"{key}) {value}")

                print()
                # Ask user for menu selection
                choice = input("Type in your choice:")
                print()
                if choice in menu_options.keys():   # Validate user choice
                    return self._select_menu(choice)    # Route to selected option
                else:
                    raise ValueError()  # Force error for invalid input
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
        page = 0    # Start at first page
        page_size = 3   # Show 3 results per page
        # Get total matching games
        total = self.game_service.get_designer_count(name)
        attempts = 0    # Track invalid attempts
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                start = page * page_size    # Calculate result start index
                # Fetch paginated results
                result = self.game_service.get_game_by_designer(name, page, page_size)
                # Show result range
                print(f"== Results (showing {start+1}-{start+page_size} of {total})")
                if not result:  # If no games returned
                    print("No more games.")
                    if page > 0:
                        page -= 1   # Go back one page
                for item in result:
                    print(f"- ID {item["game_id"]}: {item["title"]} by {item["designer"]} ${item["unit_price"]}")
                print("Options: enter Game ID to add to cart, 'n' for next, ENTER to return")
                choice = input(">")
                if choice == "":    # If user presses ENTER
                    return  # Return to previous menu
                elif choice.lower() == "n":  # If user wants next page
                    page += 1
                else:
                    qty = int(input("Quantity:"))   # Ask quantity
                    # Add to cart
                    added = self.cart_service.save_to_cart(choice, qty)
                    print(added)
            except ValueError:
                attempts += 1
                print("Game Id or quantity is invalid. Please try again\n")

    def _search_by_title(self):
        name = input("Title word: ")    # Get search keyword
        page = 0    # Start at first page
        page_size = 3   # Results per page
        # Count matching titles
        total = self.game_service.get_title_count(name)
        attempts = 0    # Track invalid attempts
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                start = page * page_size    # Calculate start index
                # Fetch results
                result = self.game_service.get_game_by_title(name, page, page_size)
                print(f"== Results (showing {start+1}-{start+page_size} of {total})")
                if not result:  # If no more games
                    print("No more games.")
                    if page > 0:
                        page -= 1   # Go back one page
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
                    # Save to cart
                    added = self.cart_service.save_to_cart(choice, qty)
                    print(added)
            except ValueError:
                attempts += 1
                print("Game Id or quantity is invalid. Please try again\n")

    def _back(self):
        # Return to member menu
        return Route.MEMBER_MENU
