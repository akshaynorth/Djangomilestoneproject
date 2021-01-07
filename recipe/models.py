from django.db import models


class RecipeIngredient(models.Model):
    description = models.CharField(max_length=1024)


class RecipeInstruction(models.Model):
    description = models.CharField(max_length=1024)


class Recipe(models.Model):
    creation_time = models.DateTimeField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=80)

    # TODO: look into putting images into their own model
    picture = models.BinaryField()

    prep_time = models.CharField(max_lenth=80)

    # TODO: check that the description length is large enough
    short_description = models.TextField(max_length=1024)

    cook_time = models.CharField(max_length=80)

    calories = models.CharField(max_length=80)

    portions = models.CharField(max_length=80)

    ingredients = models.ManyToOneRel(RecipeIngredient)

    instructions = models.ManyToOneRel(RecipeInstruction)
