from django.db import models

from django.contrib.auth.models import User


class OrderedRecipe(models.Model):
    """Hold recipe information for ordered recipes

    No recipes should be created using this model until they are purchased. Purchased recipes are to be kept on the
    database table separate from the uploaded recipes by a user.
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

    # Foreign key to the associated registered user for the recipe
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class OrderedRecipeIngredient(models.Model):
    """Ingredients associated with an ordered recipe.

    A recipe may contains multiple ingredients. Therefore the relationship between recipe and ingredient is a
    one-to-many

    Notes
    -----
        To facilitate accessibility to the list of ingredients from the recipe model the Django related queries are
        made available. (e.g. recipe.objects.filter(ordered_ingredient__description__icontains='sugar'))
    """
    recipe = models.ForeignKey(OrderedRecipe,
                               related_name='ordered_ingredients',
                               related_query_name='ordered_ingredient',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)


class OrderedRecipeInstruction(models.Model):
    """Instructions associated with an ordered recipe

    A recipe may have multiple instructions. Therefore the relationship between recipe and instructions is a
    one-to-many.

    Notes
    -----
        To ease the access to the list of instructions from the recipe model Django related queries are
        made available. (e.g. recipe.objects.filter(ordered_instruction__description__icontains='mix'))
    """
    recipe = models.ForeignKey(OrderedRecipe,
                               related_name='ordered_instructions',
                               related_query_name='ordered_instruction',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)

