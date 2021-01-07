
from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('search_recipe', views.search_recipe, name='search_recipe'),
    path('image/<int:recipe_id>', views.download_recipe_image, name='download_recipe_image'),
    path('edit/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('view/<int:recipe_id>', views.view_recipe, name='view_recipe'),
    path('submit/<int:recipe_id>', views.submit_recipe, name='submit_recipe'),
    path('delete/<int:recipe_id>', views.delete_recipe, name='delete_recipe')

]
