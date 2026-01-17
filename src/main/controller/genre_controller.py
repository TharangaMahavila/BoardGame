from src.main.util.route import Route
from src.main.repository.game_repository import GameRepository
from src.main.repository.cart_repository import CartRepository
from src.main.service.game_service import GameService
from src.main.service.cart_service import CartService


class GenreController:
    def __init__(self, context=None):
        self.context = context
        self.game_repo = GameRepository()
        # Create game service
        self.game_service = GameService(self.context, self.game_repo)
        self.cart_repo = CartRepository()
        # Create cart service
        self.cart_service = CartService(self.context, self.cart_repo, self.game_repo)

    def start(self):
        # Get all available genres as a menu
        menu_options = self.game_service.get_all_genre()

        # Track invalid menu selections
        attempts = 0
        while True:
            if attempts == 5:  # Stop after 5 invalid attempts
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print("== Genres ==")
                for key, value in menu_options.items():
                    # Display each genre option
                    print(f"{key}) {value}")

                print()
                # Get user input
                choice = input("Pick number (or ENTER to return):")
                print()
                if choice in menu_options.keys():   # If user selected a valid genre
                    genre = menu_options.get(choice)    # Get genre name
                    return self._select_genre(genre)    # Go to genre browsing
                elif choice == "":  # If user pressed ENTER
                    return Route.MEMBER_MENU    # Return to member menu
                else:
                    raise ValueError()  # Invalid input
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_genre(self, genre):
        page = 0    # Current page number
        page_size = 2   # Number of games per page

        # Total number of games in this genre
        total = self.game_service.get_genre_count(genre)

        # Track invalid attempts
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                start = page * page_size    # Calculate start index

                # Fetch paginated results
                result = self.game_service.get_game_by_genre(genre, page, page_size)

                # Show page info
                print(f"== {genre} (showing {start+1}-{start+page_size} of {total})")
                if not result:  # If no games returned
                    print("No more games.")
                    if page > 0:
                        page -= 1   # Go back one page

                for item in result:  # Display each game
                    print(f"- ID {item["game_id"]}: {item["title"]} by {item["designer"]} ${item["unit_price"]}")

                print("Options: enter Game ID to add to cart, 'n' for next, ENTER to return")
                choice = input(">")
                if choice == "":
                    return  # Return to previous menu
                elif choice.lower() == "n":  # Move to next page
                    page += 1
                else:
                    qty = int(input("Quantity:"))   # Ask quantity
                    # Add game to cart
                    added = self.cart_service.save_to_cart(choice, qty)
                    print(added)
            except ValueError:
                attempts += 1
                print("Game Id or quantity is invalid. Please try again\n")
