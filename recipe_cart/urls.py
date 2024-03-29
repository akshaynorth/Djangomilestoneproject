from django.urls import path
from . import views

urlpatterns = [
    path('shop', views.shop_page, name='shop_page'),
    path('add/<int:recipe_id>', views.add_to_cart, name='add_to_cart'),
    path('delete/<int:recipe_id>', views.delete_from_cart, name='delete_from_cart'),
]

