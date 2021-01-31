

class RecipeCartItem:
    """Holds information about a recipe in the cart"""

    def __init__(self):
        self.item_id = ''
        self.description = ''
        self.price = 0.0
        self.quantity = 0

    def as_dict(self):
        """Convert the recipe item into a dictionary that can be serialized

        Returns
        -------
        dict
            The recipe cart item represented as dictionary to facilitate serialization

        """
        return {
            'item_id': self.item_id,
            'description': self.description,
            'price': float(self.price),
            'quantity': self.quantity
        }


class RecipeCart:
    def __init__(self, cart_dict=None):
        """Initialize the recipe cart

        Parameters
        ----------
        cart_dict: dict
            The dictionary representation of a recipe cart. The recipe cart is to be serialized so that it can be stored
            in an HTTP session (for example). T?his dictionary is used to initialize the values of the recipe cart
        """

        if cart_dict:
            self.num_items = cart_dict.get('num_items')
            self.cart_items = []

            self.total = 0.0
            # Get the recipe cart items as a list and add each to the recipe cart items list
            for cart_item in cart_dict.get('cart_items', []):
                recipe_item = RecipeCartItem()
                recipe_item.item_id = cart_item.get('item_id')
                recipe_item.description = cart_item.get('description')
                recipe_item.price = cart_item.get('price')
                recipe_item.quantity = cart_item.get('quantity')
                self.cart_items.append(recipe_item)

                # Recompute the total to ensure total integrity
                self.total = self.total + float(recipe_item.price) * recipe_item.quantity
        else:
            # No initialization dictionary provided, set all values to corresponding "empty" values
            self.num_items = 0
            self.cart_items = []
            self.total = 0.0

    def add_item(self, cart_item):
        """Add a recipe item to the cart

        Parameters
        ----------
        cart_item: RecipeCartItem
            A representation of a recipe to be adde to the cart

        Returns
        -------
            None
        """
        cart_item.item_id = str(cart_item.item_id)
        for added_cart_item in self.cart_items:
            if added_cart_item.item_id == cart_item.item_id:
                # Do not add duplicate items to the cart
                return

        self.cart_items.append(cart_item)

        self.num_items = self.num_items + 1
        self.total = self.total + float(cart_item.price) * cart_item.quantity

    def delete_item(self, item_id):
        """Delete a recipe from the cart

        Parameters
        ----------
        item_id: int
            The item id of the recipe. This can be technically a string but it is meant to be a primary key from the
            backend from which recipes can be matched.

        Notes
        -----
            The recipe id is represented by the item_id. The serialization of the object bring some challenges with
            data conversion and values can be more easily matched if the comparisons are made as strings.

        Returns
        -------
            None
        """

        # Convert the item_id to string to ease comparison against the string data type
        item_id_str = str(item_id)
        for cart_item in self.cart_items:
            if cart_item.item_id == item_id_str:
                self.cart_items.remove(cart_item)
                self.num_items = self.num_items - 1 if self.num_items > 0 else 0

                self.total = self.total - float(cart_item.price) * cart_item.quantity
                # Do not let the total go below 0
                if self.total < 0.0:
                    self.total = 0.0
                break

    def as_dict(self):
        """Convert the recipe cart to a dictionary

        Returns
        -------
        dict
            The representation of the recipe cart as a dictionary to ease serialization
        """
        return {
            'num_items': self.num_items,
            'cart_items': [cart_item.as_dict() for cart_item in self.cart_items],
            'total': float(self.total)
        }
