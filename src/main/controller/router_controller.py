import sys
from src.main.context.app_context import AppContext
from src.main.controller.login_controller import LoginController
from src.main.controller.member_menu_controller import MemberMenu
from src.main.controller.genre_controller import GenreController
from src.main.controller.designer_controller import DesignerController
from src.main.controller.cart_controller import CartController
from src.main.controller.invoice_controller import InvoiceController
from src.main.util.route import Route


class RouterController:
    def __init__(self):
        # Create a shared application context
        self.context = AppContext()
        # Map each route to its corresponding controller
        self.controllers = {
            Route.LOGIN: LoginController(self.context),
            Route.MEMBER_MENU: MemberMenu(self.context),
            Route.GENRE: GenreController(self.context),
            Route.DESIGNER: DesignerController(self.context),
            Route.CART: CartController(self.context),
            Route.INVOICE: InvoiceController(self.context),
        }

    def start(self):
        # Start the application at the login screen
        route = Route.LOGIN

        while route != Route.EXIT:  # Continue until EXIT route is returned
            # Get the controller for the current route
            controller = self.controllers[route]
            # Run the controller and get the next route
            direction = controller.start()
            if direction:
                # Update route if a new one is returned
                route = direction

        print("Thank you for using Boardgame Shop!")
        sys.exit(0)  # Exit the program
