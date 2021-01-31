
import logging
import json
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

        session_cart_json = request.session.get('cart', None)

        if session_cart_json:

            session_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))
        else:
            session_cart = cart.RecipeCart()

        cart_item = cart.RecipeCartItem()
        cart_item.quantity = 2
        cart_item.price = 2.50
        cart_item.description = 'A sample recipe in cart'

        session_cart.add_item(cart_item)

        request.session['cart'] = json.dumps(session_cart.as_dict())

    except Exception:
        logger.exception('Could not find recipes')

    return render(
        request,
        'shop.html',
        context=dict(recipes=recipes, recipe_cart=session_cart)
    )


@login_required()
def add_to_cart(request, recipe_id):
    context_dict = dict()

    session_cart_json = request.session.get('cart', None)
    if session_cart_json:
        recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

    else:
        recipe_cart = cart.RecipeCart()

    if request.method == 'POST':
        # Get the product information from the database
        recipe = Recipe.objects.filter(
            ~Q(user=request.user),
            id=recipe_id
        ).first()

        if recipe:
            cart_item = cart.RecipeCartItem()

            # Avoid charging more than once for the same recipe
            cart_item.quantity = 1
            cart_item.item_id = recipe_id
            cart_item.price = recipe.price
            cart_item.description = recipe.name

            recipe_cart.add_item(cart_item)

    request.session['cart'] = json.dumps(recipe_cart.as_dict())

    # Add the product item to the session
    context_dict.update(
        dict(
            recipes=Recipe.objects.filter(~Q(user=request.user)),
            recipe_cart=recipe_cart
        )
    )

    return render(
        request,
        'shop.html',
        context=context_dict
    )


@login_required()
def delete_from_cart(request, recipe_id):
    context_dict = dict()

    session_cart_json = request.session.get('cart', None)
    if session_cart_json:
        recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

    else:
        recipe_cart = cart.RecipeCart()

    if request.method == 'POST':
        # Get the product information from the database
        recipe = Recipe.objects.filter(
            ~Q(user=request.user),
            id=recipe_id
        ).first()

        if recipe:
            recipe_cart.delete_item(recipe_id)

        request.session['cart'] = json.dumps(recipe_cart.as_dict())

        # Add the product item to the session
        context_dict.update(
            dict(
                recipes=Recipe.objects.filter(~Q(user=request.user)),
                recipe_cart=recipe_cart
            )
        )

        return render(
            request,
            'shop.html',
            context=context_dict
        )
