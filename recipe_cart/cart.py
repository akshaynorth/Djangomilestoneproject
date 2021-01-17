

class RecipeCartItem:

    def __init__(self):
        self.description = ''
        self.price = 0.0
        self.quantity = 0


class RecipeCart:
    def __init__(self):
        self.num_items = 0
        self.cart_items = {}
        self.total = 0.0

    def add_item(self, cart_item):
        self.cart_items.update(
            dict(item_id=cart_item)
        )
        self.num_items = self.num_items + 1
        self.total = self.total + cart_item.price * cart_item.quantity

    def delete_item(self, item_id):
        if item_id in self.cart_items:
            del self.cart_items[item_id]
            self.num_items = self.num_items - 1 if self.num_items > 0 else 0
