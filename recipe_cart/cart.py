

class RecipeCartItem:

    def __init__(self):
        self.item_id = ''
        self.description = ''
        self.price = 0.0
        self.quantity = 0

    def as_dict(self):
        return {
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity
        }


class RecipeCart:
    def __init__(self, cart_dict=None):

        if cart_dict:
            self.num_items = cart_dict.get('num_items')
            self.cart_items = []

            self.total = 0.0
            for cart_item in cart_dict.get('cart_items', []):
                recipe_item = RecipeCartItem()
                recipe_item.item_id = cart_item.get('item_id')
                recipe_item.description = cart_item.get('description')
                recipe_item.price = cart_item.get('price')
                recipe_item.quantity = cart_item.get('quantity')
                self.cart_items.append(recipe_item)

                self.total = self.total + recipe_item.price * recipe_item.quantity
        else:
            self.num_items = 0
            self.cart_items = []
            self.total = 0.0

    def add_item(self, cart_item):

        for added_cart_item in self.cart_items:
            if added_cart_item.item_id == cart_item.item_id:
                # Do not add duplicate items to the cart
                return

        self.cart_items.append(cart_item)

        self.num_items = self.num_items + 1
        self.total = self.total + cart_item.price * cart_item.quantity

    def delete_item(self, item_id):
        for cart_item in self.cart_items:
            if cart_item.item_id == item_id:
                self.cart_items.remove(cart_item)
                self.num_items = self.num_items - 1 if self.num_items > 0 else 0
                break

    def as_dict(self):
        return {
            'item_id': self.item_id,
            'num_items': self.num_items,
            'cart_items': [cart_item.as_dict() for cart_item in self.cart_items],
            'total': self.total
        }
