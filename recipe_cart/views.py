
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
    """Render the shopping page

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Notes
    -----
        Users are only presented with the recipes other users have registered. This is to avoid a user buying their
        own uploaded recipes.

        To purchase recipes, users are required to be registered and logged in.

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """

    session_cart = None
    try:
        # Obtain the list of recipes uploaded by other users
        recipes = Recipe.objects.filter(~Q(user=request.user))

        # Obtain the recipe cart from the session. Create it if it does not exist
        session_cart_json = request.session.get('cart', None)
        if session_cart_json:
            session_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))
        else:
            session_cart = cart.RecipeCart()

        # Store the cart object in the session. Serialize as a JSON string as the HTTP session only accepts built-in
        # data types
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
    """Add a recipe to the cart

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The id of the recipe to add to the cart

    Notes
    -----
        This function maintains the existence of the recipe cart in the HTTP session. When the requested recipe
        does not exist or belongs to the logged in user, it is not added to the cart.

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. The user is redirected to the shopping page.
    """
    context_dict = dict()

    try:
        session_cart_json = request.session.get('cart', None)
        if session_cart_json:
            recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

        else:
            recipe_cart = cart.RecipeCart()

        if request.method == 'POST':
            # Get the product information from the database for the provided user and ensure that it does not belong to
            # the logged in user
            recipe = Recipe.objects.filter(
                ~Q(user=request.user),
                id=recipe_id
            ).first()

            # Proceed to add the recipe to the cart if a recipe was found
            if recipe:
                cart_item = cart.RecipeCartItem()

                # Avoid charging more than once for the same recipe
                cart_item.quantity = 1
                cart_item.item_id = recipe_id
                cart_item.price = recipe.price
                cart_item.description = recipe.name

                recipe_cart.add_item(cart_item)

        request.session['cart'] = json.dumps(recipe_cart.as_dict())

    except:
        logger.exception('Could not add recipe to cart')

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
    """Delete a recipe from the cart

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The id of the recipe to delete

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. The user is redirected to the shopping page
    """
    context_dict = dict()

    try:
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
    except:
        logger.exception('Could not delete from cart')

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
