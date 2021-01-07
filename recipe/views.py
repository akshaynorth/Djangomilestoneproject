from django.shortcuts import render

# Create your views here.

import json
import logging
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Recipe, RecipeIngredient, RecipeInstruction

logger = logging.getLogger(__name__)


@csrf_protect
def create(requests):
    try:
        if requests.method == 'POST':
            form_data = requests.POST
            recipe = Recipe.objects.create(
                creation_time=datetime.datetime.now(),
                name=form_data.get('name', ''),
                type=form_data.get('type', ''),
                short_description=form_data.get('recipe_desc', ''),
                prep_time=form_data.get('prep_time', ''),
                cook_time=form_data.get('cook_time', ''),
                calories=form_data.get('calories', ''),
                portions=form_data.get('portions', ''),
            )

            for ingredient in json.loads(form_data.get('ingredients', '[]')):
                RecipeIngredient.objects.create(
                    description=ingredient,
                    recipe=recipe
                )

            for instruction in json.loads(form_data.get('instructions', '[]')):
                RecipeInstruction.objects.create(
                    description=instruction,
                    recipe=recipe
                )
        else:
            raise ValueError('Invalid HTTP method GET for recipe create')

    except Exception as e:
        logger.exception('Could not create recipe')
        return JsonResponse(
            dict(error=str(e)),
            status=404
        )

    return JsonResponse(
        dict()
    )


def search_recipe(requests):
    return None


def download_recipe_image(requests, recipe_id):
    return None


def edit_recipe(requests, recipe_id):
    return None


def view_recipe(requests, recipe_id):
    return None


def submit_recipe(requests, recipe_id):
    return None


def delete_recipe(requests, recipe_id):
    return None
