from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:item_id>', views.add_to_cart, 'add_to_cart'),
    path('delete/<int:item_id>', views.delete_from_cart, 'delete_from_cart'),
]
