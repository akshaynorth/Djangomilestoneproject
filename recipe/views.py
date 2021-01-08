from django.shortcuts import render

# Create your views here.

import json
import logging
import datetime

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
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

            if requests.FILES.get('file', None):
                uploaded_file = requests.FILES.get('file')

                # Upload file in 1 MB chunks
                image_buffer = bytearray()
                for file_chunk in uploaded_file.chunks(2**20):
                    image_buffer += file_chunk

                recipe.picture = image_buffer

                recipe.save()

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


@csrf_protect
def search_recipe(requests):
    try:
        if requests.method == 'POST':
            form_data = requests.POST

            query_dict = dict()

            recipe_type = form_data.get('type', None)
            if recipe_type and recipe_type.upper() != 'ALL':
                query_dict.update(
                    dict(
                      type=recipe_type
                    )
                )

            ingredient_list = form_data.get('ingredient_list', None)
            ingredient_query_args = None

            if ingredient_list:
                ingredient_search_type = form_data.get('ingredient_search_type', None)
                if ingredient_search_type and ingredient_search_type.upper() != 'ALL':
                    query_dict.update(
                        dict(ingredient__in=ingredient_list)
                    )
                else:
                    for ingredient in ingredient_list:
                        if ingredient_query_args:
                            ingredient_query_args = ingredient_query_args[0] & Q(ingredient_icontains=ingredient)

                        else:
                            ingredient_query_args = (
                                Q(ingredient__icontains=ingredient),
                            )

            if ingredient_query_args:
                recipes = Recipe.objects.filter(ingredient_query_args, query_dict)
            else:
                recipes = Recipe.objects.filter(query_dict)

            return render(
                'pages/submit-recipe.html',
                recipe_list=recipes
            )

        else:
            raise ValueError('Only HTTP POST supported for search recipes')
    except Exception as e:
        logger.exception('Could not complete search for recipe')
        raise Http404('Could not search recipe: {}'.format(str(e)))

    raise Http404('Unexpected error has occurred while searching for recipe')


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
