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
        # Initialize cart service
        self.cart_service = CartService(self.context, self.cart_repo, self.game_repo)
        # Initialize order service
        self.order_service = OrderService(self.context, self.order_repo)

    def start(self):
        print("*"*50)
        print(f"***{"Welcome to the Online Boardgame Shop":^44}***")
        print("*"*50)
        print()
        print("Current Cart Contents:\n")

        # Get all items currently in the cart
        items = self.cart_service.get_all_cart_items()
        if items:  # If cart is not empty
            print(f"{"Game ID":<10} {"Title":<50} {"$":>6} {"Qty":>4} {"Total":>6}")
            print("-"*80)
            total = 0  # Initialize total cart value
            for item in items:
                # Calculate total price for this item
                item_total = item["unit_price"] * item["quantity"]
                # Add to cart total
                total += item_total
                print(f"{item["game_id"]:<10} {item["title"]:<50} {item["unit_price"]:>6} {item["quantity"]:>4} {item_total:>6}")
            print("-"*80)
            print()
            print(f"Total = ${total}\n")
            choice = input("Proceed to checkout (Y/N)? ")
            if choice.lower() == "y":   # If user chooses to checkout
                # Save the order
                self.order_service.save_order()
                # Navigate to invoice screen
                return Route.INVOICE
            else:
                # Go back to member menu
                return Route.MEMBER_MENU
        else:
            print("Cart is empty.")
            # Return to member menu
            return Route.MEMBER_MENU
