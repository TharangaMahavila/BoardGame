import sys
from src.main.context.app_context import AppContext
from src.main.controller.login_controller import LoginController
from src.main.controller.member_menu_controller import MemberMenu
from src.main.controller.genre_controller import GenreController
from src.main.util.route import Route


class RouterController:
    def __init__(self):
        self.context = AppContext()
        self.controllers = {
            Route.LOGIN: LoginController(self.context),
            Route.MEMBER_MENU: MemberMenu(self.context),
            Route.GENRE: GenreController(self.context),
        }

    def start(self):
        route = Route.LOGIN

        while route != Route.EXIT:
            controller = self.controllers[route]
            direction = controller.start()
            if direction:
                route = direction

        print("Thank you for using Boardgame Shop!")
        sys.exit(0)
