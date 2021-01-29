
import logging
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.db.models import Q

from recipe.models import Recipe

from . import cart

logger = logging.getLogger(__name__)


@login_required()
def shop_page(request):

    session_cart = None
    try:
        recipes = Recipe.objects.filter(~Q(user=request.user))

        session_cart_dict = request.session.get('cart', None)

        if session_cart_dict:
            session_cart = cart.RecipeCart(cart_dict=session_cart_dict)

        session_cart = cart.RecipeCart()

        cart_item = cart.RecipeCartItem()
        cart_item.quantity = 2
        cart_item.price = 2.50
        cart_item.description = 'A sample recipe in cart'

        session_cart.add_item(cart_item)

        # request.session['cart'] = session_cart.as_dict()

    except Exception:
        logger.exception('Could not find recipes')

    return render(
        request,
        'shop.html',
        context=dict(recipes=recipes, recipe_cart=session_cart)
    )


@login_required()
def add_to_cart(request, item_id):
    context_dict = dict()
    if request.method == 'POST':
        session_cart = request.session.get('cart', None)
        if session_cart is None:
            session_cart = cart.RecipeCart()

        # Get the product information from the database

        # Add the product item to the session
        context_dict.update(
            dict(cart=session_cart)
        )
    else:
        pass


@login_required()
def delete_from_cart(request, item_id):
    context_dict = dict()

    if request.method == 'POST':
        session_cart = request.session.get('cart', None)

        if session_cart is not None:
            session_cart.delete_item(item_id)

        # Update the session with the deletion of the item
        context_dict.update(dict(cart=session_cart))
    else:
        pass
