class OrderService:
    def __init__(self, context=None, order_repo=None):
        self.context = context
        self.orderRepo = order_repo

    def save_order(self):
        # Creates a new order using the current logged-in user's data
        # Returns the newly created order number
        order_number = self.orderRepo.save_order(self.context.user)
        return order_number

    def get_order(self):
        # Retrieves the most recent order placed by the current user
        return self.orderRepo.get_order_by_user_id(self.context.user["user_id"])

    def get_order_items_by_order_id(self, order_id):
        # Retrieves all items belonging to a given order
        return self.orderRepo.get_order_items_by_order_id(order_id)
