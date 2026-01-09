class OrderService:
    def __init__(self, context=None, order_repo=None):
        self.context = context
        self.orderRepo = order_repo

    def save_order(self):
        order_number = self.orderRepo.save_order(self.context.user)
        return order_number

    def get_order(self):
        return self.orderRepo.get_order_by_user_id(self.context.user["user_id"])

    def get_order_items_by_order_id(self, order_id):
        return self.orderRepo.get_order_items_by_order_id(order_id)
