from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from . import cart


@login_required()
def shop_page(request):
    return render(
        request,
        'shop.html'
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
