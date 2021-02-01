
from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_ordered_recipes, name='show_ordered_recipes'),
    path('view/<int:recipe_id>', views.view_ordered_recipe, name='view_order_recipe'),
    path('image/<int:recipe_id>', views.download_ordered_recipe_image, name='view_ordered_recipe_image')
]
