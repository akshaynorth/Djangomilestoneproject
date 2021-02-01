import stripe

import json
import os
import math
import logging
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.urls import reverse

from recipe_cart import cart

from recipe.models import Recipe
from recipe_orders.models import OrderedRecipe, OrderedRecipeIngredient, OrderedRecipeInstruction

# Obtain Stripe Secret API Key from the environment
stripe.api_key = os.environ.get('STRIPE_API_KEY', '')


logger = logging.getLogger(__name__)


@login_required()
def order_review(request):
    """Renders the order review page

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    context_dict = dict()

    # Get the recipes stored in the session cart
    session_cart_json = request.session.get('cart', None)
    if session_cart_json:
        recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

    else:
        recipe_cart = cart.RecipeCart()

    context_dict.update(
        dict(recipe_cart=recipe_cart)
    )

    return render(
        request,
        'checkout.html',
        context=context_dict,
    )


def payment_success(request):
    """Payment success page for Stripe payment success redirection

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Notes
    -----
        Success page to be rendered by the payment integration with Stripe. The page needs to be publicly accessible
        as required by Stripe. Therefore, no login is required

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """

    if request.method == 'GET' and request.user.is_authenticated:
        # Obtained code from Stripe for checkout session retrieval: See:
        # https://stripe.com/docs/payments/checkout/custom-success-page
        session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
        customer = stripe.Customer.retrieve(session.customer)

        if not customer.name:
            # If the customer name can not be retrieved, interpret it as an attempt to hijack the Stripe session
            # and raise an error
            raise ValueError('Could not obtain customer name from Stripe payment')

        # The user has paid an is authenticated. Proceed to add the ordered recipes to its profile of ordered lists
        # Get the recipes in the cart
        session_cart_json = request.session.get('cart', None)

        if session_cart_json is None:
            # User has paid and authenticated but no shopping cart, no recipes to add to ordered list.
            # this condition is a candidate to a refund and should never occur.
            raise Http404()

        recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

        for cart_item in recipe_cart.cart_items:

            recipe = Recipe.objects.get(id=int(cart_item.item_id))

            ordered_recipe = OrderedRecipe.objects.create(
                creation_time=datetime.datetime.now(),
                name=recipe.name,
                type=recipe.type,
                short_description=recipe.short_description,
                prep_time=recipe.prep_time,
                cook_time=recipe.cook_time,
                calories=recipe.calories,
                portions=recipe.portions,
                price=recipe.price,
                user=request.user
            )

            for ingredient in recipe.ingredients.all():
                OrderedRecipeIngredient.create(
                    recipe=ordered_recipe,
                    description=ingredient.description
                )

            for instruction in recipe.instructions.all():
                OrderedRecipeInstruction.create(
                    recipe=ordered_recipe,
                    description=instruction.description
                )

        # Clear the session cart now that all ordered recipes were purchased and stored
        request.session['cart'] = json.dumps(cart.RecipeCart().as_dict())

    else:
        logger.exception('Could not complete payment success activities')
        raise Http404()

    return render(
        request,
        'pay_success.html'
    )


def payment_cancel(request):
    """Payment cancel page for Stripe payment cancel redirection

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Notes
    -----
        Cancel page to be rendered by the payment integration with Stripe. The page needs to be publicly accessible
        as required by Stripe. Therefore, no login is required

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    return render(
        request,
        'pay_cancel.html'
    )


@login_required()
def create_checkout_session(request):
    """Create a checkout payment session intent with Stripe

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Notes
    -----
        Stripe requires a very specific URL for the create session. (/create-checkout-session). During testing, it
        was found that any other endpoint would result in an invalid URL error response from Stripe.

        The items to be paid for are obtained from the recipe cart in the HTTP session.

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'POST':
            session_cart_json = request.session.get('cart', None)

            if session_cart_json:
                line_items_list = []
                recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

                # Add the recipe cart items to the Stripe request
                for cart_item in recipe_cart.cart_items:
                    line_items_list.append(
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': cart_item.description,
                                },
                                'unit_amount': math.ceil(cart_item.price * 100),
                            },
                            'quantity': cart_item.quantity
                        }
                    )

                if line_items_list:
                    session = stripe.checkout.Session.create(
                      payment_method_types=['card'],
                      line_items=line_items_list,
                      mode='payment',
                      # success_url has to be absolute as required by Stripe
                      success_url='{}?session_id={CHECKOUT_SESSION_ID}'.format(
                          request.build_absolute_uri(reverse('pay_success'))
                      ),
                      # cancel_url has to be absolute as required by Stripe
                      cancel_url=request.build_absolute_uri(reverse('pay_cancel')),
                    )

                    return JsonResponse(dict(id=session.id))

    except:
        logger.exception('Could not create checkout session')

    # Return a bogus session id as a signal of an error
    return JsonResponse(dict(id=''))
