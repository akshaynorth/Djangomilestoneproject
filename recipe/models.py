from django.db import models

from django.contrib.auth.models import User


class Recipe(models.Model):
    """Hold recipe information

    The recipes are associated with registered users. Users should not buy their own recipes nor select them for
    purchase. Users should also only be able to manage (Create, Update, Delete) their registered recipes and not other
    user recipes.
    """
    creation_time = models.DateTimeField()
    # The name of the recipe
    name = models.CharField(max_length=255)

    # Recipe category, (e.g. Lunch, Breakfast, etc.)
    type = models.CharField(max_length=80)

    # Optional recipe picture
    picture = models.BinaryField()

    # Recipe preparation time a string that should include the unit (e.g. 1 hr)
    prep_time = models.CharField(max_length=80)

    # Recipe description. A paragraph that describes the recipe as to call the attention of others wanting to make it
    short_description = models.TextField(max_length=1024)

    # The amount of cooking time for the recipe
    cook_time = models.CharField(max_length=80)

    # The amount of calories in the recipe
    calories = models.CharField(max_length=80)

    # The number of people that could be potentially fed with the recipe proportions
    portions = models.CharField(max_length=80)

    # The price to sell the recipe for. Should not contain any special characters only numbers and decimals
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # Foreign key to the associated registered user for the recipe
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class RecipeIngredient(models.Model):
    """Ingredients associated with a recipe.

    A recipe may contains multiple ingredients. Therefore the relationship between recipe and ingredient is a
    one-to-many

    Notes
    -----
        To facilitate accessibility to the list of ingredients from the recipe model the Django related queries are
        made available. (e.g. recipe.objects.filter(ingredient__description__icontains='sugar'))
    """
    recipe = models.ForeignKey(Recipe,
                               related_name='ingredients',
                               related_query_name='ingredient',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)


class RecipeInstruction(models.Model):
    """Instructions associated with a recipe

    A recipe may have multiple instructions. Therefore the relationship between recipe and instructions is a
    one-to-many.

    Notes
    -----
        To ease the access to the list of instructions from the recipe model Django related queries are
        made available. (e.g. recipe.objects.filter(instruction__description__icontains='mix'))
    """
    recipe = models.ForeignKey(Recipe,
                               related_name='instructions',
                               related_query_name='instruction',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
