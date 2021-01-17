
from django.urls import re_path, path
from . import views

urlpatterns = [
    path('success', views.payment_success, 'pay_success'),
    re_path('^create-checkout-session/$', views.create_checkout_session, 'create_checkout_session'),
]
