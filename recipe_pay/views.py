import stripe

import json
import os
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from recipe_cart import cart


stripe.api_key = os.environ.get('STRIPE_API_KEY', '')


logger = logging.getLogger(__name__)


@login_required()
def order_review(request):
    context_dict = dict()

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
    return render(
        request,
        'pay_success.html'
    )


def payment_cancel(request):
    return render(
        request,
        'pay_cancel.html'
    )


@login_required()
def create_checkout_session(request):
    try:
        if request.method == 'POST':
            session_cart_json = request.session.get('cart', None)

            if session_cart_json:
                line_items_list = []
                recipe_cart = cart.RecipeCart(cart_dict=json.loads(session_cart_json))

                for cart_item in recipe_cart.cart_items:
                    line_items_list.append(
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': cart_item.description,
                                },
                                'unit_amount': int(cart_item.price * 100),
                            },
                            'quantity': cart_item.quantity
                        }
                    )

                if line_items_list:
                    session = stripe.checkout.Session.create(
                      payment_method_types=['card'],
                      line_items=line_items_list,
                      mode='payment',
                      success_url=request.build_absolute_uri(reverse('pay_success')),
                      cancel_url=request.build_absolute_uri(reverse('pay_cancel')),
                    )

                    return JsonResponse(dict(id=session.id))

    except:
        logger.exception('Could not create checkout session')

    # Return a bogus session id as a signal of an error
    return JsonResponse(dict(id=''))
