import stripe

import json
import os
import math
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse

from recipe_cart import cart


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
                      success_url=request.build_absolute_uri(reverse('pay_success')),
                      # cancel_url has to be absolute as required by Stripe
                      cancel_url=request.build_absolute_uri(reverse('pay_cancel')),
                    )

                    # Clear out the cart as user is proceeding to payment
                    request.session['cart'] = json.dumps(cart.RecipeCart().as_dict())

                    return JsonResponse(dict(id=session.id))

    except:
        logger.exception('Could not create checkout session')

    # Return a bogus session id as a signal of an error
    return JsonResponse(dict(id=''))
