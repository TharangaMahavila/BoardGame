class CartService:
    def __init__(self, context=None, cart_repo=None, game_repo=None):
        self.context = context
        self.cartRepo = cart_repo
        self.gameRepo = game_repo

    def save_to_cart(self, game_id, qty):
        if qty < 1:
            raise ValueError("Invalid quantity")
        game = self.gameRepo.find_by_id(game_id)
        if not game:
            raise ValueError("Game id is invalid")
        exist = self.cartRepo.get_by_user_id_and_game_id(self.context.user["user_id"], game_id)
        if exist:
            result = self.cartRepo.update_item(self.context.user["user_id"], game_id, qty)
            if result == 1:
                return "Updated the cart"
        else:
            result = self.cartRepo.save_item(self.context.user["user_id"], game_id, qty)
            if result == 1:
                return "Added to cart"
