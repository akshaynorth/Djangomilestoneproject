from django.db import models


from recipe.models import Recipe, RecipeIngredient, RecipeInstruction


class OrderedRecipe(Recipe):
    """Hold recipe information for ordered recipes

    No recipes should be created using this model until they are purchased. Purchased recipes are to be kept on the
    database table separate from the uploaded recipes by a user.

    A purchased recipe is almost identical to an uploaded recipe except for maybe the price which does not need to be
    kept for the purpose of this application. To complete this implementation in an easier fashion, we are inheriting
    the fields of the Recipe model.
    """
    pass


class OrderedRecipeIngredient(RecipeIngredient):
    """Ingredients associated with an ordered recipe.

    A recipe may contains multiple ingredients. Therefore the relationship between recipe and ingredient is a
    one-to-many

    Notes
    -----
        To facilitate accessibility to the list of ingredients from the recipe model the Django related queries are
        made available. (e.g. recipe.objects.filter(ingredient__description__icontains='sugar'))
    """
    recipe = models.ForeignKey(OrderedRecipe,
                               related_name='ingredients',
                               related_query_name='ingredient',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)


class OrderedRecipeInstruction(RecipeInstruction):
    """Instructions associated with an ordered recipe

    A recipe may have multiple instructions. Therefore the relationship between recipe and instructions is a
    one-to-many.

    Notes
    -----
        To ease the access to the list of instructions from the recipe model Django related queries are
        made available. (e.g. recipe.objects.filter(instruction__description__icontains='mix'))
    """
    recipe = models.ForeignKey(OrderedRecipe,
                               related_name='instructions',
                               related_query_name='instruction',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)

