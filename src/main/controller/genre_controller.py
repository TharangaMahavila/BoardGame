from src.main.util.route import Route
from src.main.repository.genre_repository import GenreRepository
from src.main.service.genre_service import GenreService


class GenreController:
    def __init__(self, context=None):
        self.context = context
        self.genre_repo = GenreRepository()
        self.genre_service = GenreService(self.context, self.genre_repo)

    def start(self):
        menu_options = self.genre_service.get_all_genre()

        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                print("== Genres ==")
                for key, value in menu_options.items():
                    print(f"{key}) {value}")

                print()
                choice = input("Pick number (or ENTER to return):")
                print()
                if choice in menu_options.keys():
                    genre = menu_options.get(choice)
                    return self._select_genre(genre)
                elif choice == "":
                    return Route.MEMBER_MENU
                else:
                    raise ValueError()
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_genre(self, genre):
        page = 0
        page_size = 2
        total = self.genre_service.get_genre_count(genre)
        while True:
            start = page * page_size
            result = self.genre_service.get_game_by_genre(genre, page, page_size)
            print(f"== {genre} (showing {start+1}-{start+page_size} of {total})")
            if not result:
                print("No more games.")
                page -= 1
            for item in result:
                print(f"- ID {item["game_id"]}: {item["title"]} by {item["designer"]} ${item["unit_price"]}")
            print("Options: enter Game ID to add to cart, 'n' for next, ENTER to return")
            choice = input(">")
            if choice == "":
                return
            elif choice.lower() == "n":
                page += 1
