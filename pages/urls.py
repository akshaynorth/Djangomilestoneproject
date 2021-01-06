from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='home'),
    path('recipe-page-1.html', views.recipe1, name='recipe1'),
    path('recipe-page-2.html', views.recipe2, name='recipe2'),
    path('recipe-page-3.html', views.recipe3, name='recipe3'),
    path('recipe-page-4.html', views.recipe4, name='recipe4'),
    path('recipe-page-5.html', views.recipe5, name='recipe5'),
    path('browse-recipes.html', views.search, name='search'),
    path('submit-recipe.html', views.submit_recipe, name='submit_recipe')
]
