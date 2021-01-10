from django.contrib import admin

from .views import Recipe, RecipeIngredient, RecipeInstruction

# Register your models here.

admin.register(Recipe, RecipeIngredient, RecipeInstruction)
