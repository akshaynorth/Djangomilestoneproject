
from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_ordered_recipes, name='show_ordered_recipes'),
]
