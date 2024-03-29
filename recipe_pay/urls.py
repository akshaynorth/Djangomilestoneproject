
from django.urls import re_path, path
from . import views

urlpatterns = [
    path('success', views.payment_success, name='pay_success'),
    path('pay_cancel', views.payment_cancel, name='pay_cancel'),
    path('order_review', views.order_review, name='order_review'),
    # mapped from main site URL as create checkout session
    path('', views.create_checkout_session, name='create_checkout_session'),
]
