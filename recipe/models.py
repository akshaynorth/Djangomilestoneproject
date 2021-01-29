from django.db import models

from django.contrib.auth.models import User


class Recipe(models.Model):
    creation_time = models.DateTimeField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=80)

    picture = models.BinaryField()

    prep_time = models.CharField(max_length=80)

    # TODO: check that the description length is large enough
    short_description = models.TextField(max_length=1024)

    cook_time = models.CharField(max_length=80)

    calories = models.CharField(max_length=80)

    portions = models.CharField(max_length=80)

    price = models.DecimalField(max_digits=5, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               related_name='ingredients',
                               related_query_name='ingredient',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(Recipe,
                               related_name='instructions',
                               related_query_name='instruction',
                               on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
