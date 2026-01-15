class CartService:
    def __init__(self, context=None, cart_repo=None, game_repo=None):
        self.context = context
        self.cartRepo = cart_repo
        self.gameRepo = game_repo

    def save_to_cart(self, game_id, qty):
        # Quantity must be at least 1
        if qty < 1:
            raise ValueError("Invalid quantity")
        # Check whether the game exists in the database
        game = self.gameRepo.find_by_id(game_id)
        if not game:
            raise ValueError("Game id is invalid")

        # Check if this game already exists in the user's cart
        exist = self.cartRepo.get_by_user_id_and_game_id(self.context.user["user_id"], game_id)
        if exist:
            # If the item already exists in the cart, update its quantity
            result = self.cartRepo.update_item(self.context.user["user_id"], game_id, qty)
            if result == 1:
                return "Updated the cart"
        else:
            # If the item does not exist, insert a new row into the cart
            result = self.cartRepo.save_item(self.context.user["user_id"], game_id, qty)
            if result == 1:
                return "Added to cart"

    def get_all_cart_items(self):
        # Retrieve all cart items for the currently logged-in user
        return self.cartRepo.get_by_user_id(self.context.user["user_id"])
