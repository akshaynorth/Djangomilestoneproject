import stripe

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.

stripe.api_key = ''


@login_required()
def payment_success(request):
    return render(
        request,
        'pay_success.html'
    )


@login_required()
def payment_cancel(request):
    return render(
        request,
        'pay_cancel.html'
    )


@login_required()
def create_checkout_session(request):
    if request.method == 'POST':
        session_cart = request.session.get('cart', None)

        if session_cart:
            line_items_list = []

            for cart_item in session_cart.cart_items.values():
                line_items_list.append(
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': cart_item.description,
                            },
                            'unit_amount': cart_item.price,
                        },
                        'quantity': cart_item.quantity
                    }
                )

            if line_items_list:
                session = stripe.checkout.Session.create(
                  payment_method_types=['card'],
                  line_items=line_items_list,
                  mode='payment',
                  success_url=reverse('pay_success'),
                  cancel_url=reverse('pay_cancel'),
                )

                return JsonResponse(dict(id=session.id))

    # Return a bogus session id as a signal of an error
    return JsonResponse(dict(id=''))
