from src.main.util.route import Route
from src.main.repository.game_repository import GameRepository
from src.main.repository.cart_repository import CartRepository
from src.main.repository.order_repository import OrderRepository
from src.main.service.cart_service import CartService
from src.main.service.order_service import OrderService


class CartController:
    def __init__(self, context=None):
        self.context = context
        self.game_repo = GameRepository()
        self.cart_repo = CartRepository()
        self.order_repo = OrderRepository()
        self.cart_service = CartService(self.context, self.cart_repo, self.game_repo)
        self.order_service = OrderService(self.context, self.order_repo)

    def start(self):
        print("*"*50)
        print(f"***{"Welcome to the Online Boardgame Shop":^44}***")
        print("*"*50)
        print()
        print("Current Cart Contents:\n")
        items = self.cart_service.get_all_cart_items()
        if items:
            print(f"{"Game ID":<10} {"Title":<50} {"$":>6} {"Qty":>4} {"Total":>6}")
            print("-"*80)
            total = 0
            for item in items:
                item_total = item["unit_price"] * item["quantity"]
                total += item_total
                print(f"{item["game_id"]:<10} {item["title"]:<50} {item["unit_price"]:>6} {item["quantity"]:>4} {item_total:>6}")
            print("-"*80)
            print()
            print(f"Total = ${total}\n")
            choice = input("Proceed to checkout (Y/N)? ")
            if choice.lower() == "y":
                self.order_service.save_order()
                return Route.INVOICE
            else:
                return Route.MEMBER_MENU
        else:
            print("Cart is empty.")
            return Route.MEMBER_MENU
