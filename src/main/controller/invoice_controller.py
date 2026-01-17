from datetime import timedelta
from src.main.util.route import Route
from src.main.repository.order_repository import OrderRepository
from src.main.service.order_service import OrderService


class InvoiceController:
    def __init__(self, context=None):
        # Store shared application context
        self.context = context
        # Create order repository
        self.order_repo = OrderRepository()
        # Create order service
        self.order_service = OrderService(self.context, self.order_repo)

    def start(self):
        # Retrieve the latest order
        order = self.order_service.get_order()

        if order:   # If an order exists
            print("="*50)
            print(f"Invoice for Order no. {order["order_no"]}")
            print("="*50)
            print()
            print(f"Name: {order["first_name"]} {order["last_name"]}")
            print(f"Address: {order["ship_street"]}, {order["ship_city"]}")
            print(f"Postcode: {order["ship_postal_code"]}")
            # Calculate delivery date
            print(f"Estimated delivery: {(order["created"] + timedelta(weeks=1)).date()}")
            print("-"*80)
            # Print table header
            print(f"{"Game ID":<10} {"Title":<50} {"$":>6} {"Qty":>4} {"Total":>6}")
            print("-"*80)

            # Fetch order items
            items = self.order_service.get_order_items_by_order_id(order["order_no"])

            total = 0   # Initialize total order cost
            for item in items:  # Loop through order items
                total += item["line_total"]  # Add each line total
                print(f"{item["game_id"]:<10} {item["title"]:<50} {item["unit_price"]:>6} {item["quantity"]:>4} {item["line_total"]:>6}")

            print("-"*80)
            print()
            print(f"Total = ${total}\n")    # Display final total
            print("="*80)

            choice = input("Press Enter to return to the main menu")
            if choice == "":
                # Go back to main menu
                return Route.MEMBER_MENU
        else:
            # If no order exists
            print("No order found.")
            return Route.MEMBER_MENU
