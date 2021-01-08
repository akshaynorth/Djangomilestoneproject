from django.shortcuts import render

# Create your views here.

import json
import logging
import datetime
import io

from django.http import JsonResponse, Http404, FileResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from .models import Recipe, RecipeIngredient, RecipeInstruction

logger = logging.getLogger(__name__)


@csrf_protect
def create(request):
    try:
        if request.method == 'POST':
            form_data = request.POST
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

            if request.FILES.get('file', None):
                uploaded_file = request.FILES.get('file')

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
def search_recipe(request):
    try:
        if request.method == 'POST':
            form_data = request.POST

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
                recipes = Recipe.objects.filter(
                    *ingredient_query_args,
                    **query_dict
                )
            else:
                recipes = Recipe.objects.filter(**query_dict)

            return render(
                request,
                'browse-recipes.html',
                context=dict(recipe_list=recipes)
            )

        else:
            raise ValueError('Only HTTP POST supported for search recipes')
    except Exception as e:
        logger.exception('Could not complete search for recipe')
        raise Http404('Could not search recipe: {}'.format(str(e)))

    raise Http404('Unexpected error has occurred while searching for recipe')


@csrf_exempt
def download_recipe_image(request, recipe_id):
    try:
        if request.method == 'GET':
            # Obtain the image from the database
            recipe = Recipe.objects.get(id=recipe_id)

            image_data = recipe.picture

            return FileResponse(
                io.BytesIO(image_data)
            )
        else:
            raise ValueError('HTTP method POST not supported for image download')

    except Exception as e:
        logger.exception('Could not download recipe image')
        raise Http404('Could not download image for recipe: {}'.format(e))

    raise Http404('Unexpected error has occurred')


@csrf_protect
def edit_recipe(request, recipe_id):
    try:
        if request.method == 'GET':
            recipe = Recipe.objects.get(id=recipe_id)

            recipe_dict = {
                'id': recipe.id,
                'name': recipe.name,
                'type': recipe.type,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'calories': recipe.calories,
                'portions': recipe.portions,
                'short_description': recipe.short_description,
                'ingredients': list(recipe.ingredients.values_list('description', flat=True)),
                'instructions': list(recipe.instructions.values_list('description', flat=True)),
            }
            return render(
                request,
                'edit-recipe.html',
                context=dict(
                    recipe=recipe_dict,
                    recipe_type_list=['All', 'Breakfast', 'Lunch', 'Beverages', 'Appetizers', 'Soups', 'Salads', 'Beef',
                                      'Poultry', 'Pork', 'Seafood', 'Vegetarian', 'Vegetables', 'Desserts', 'Canning',
                                      'Breads', 'Holidays']
                )
            )
        else:
            raise ValueError('Unsupported HTTP method for edit recipe: {}'.format(request.method))
    except Exception as e:
        logger.exception('Could not retrieve recipe information')
        raise Http404('Could not retrieve recipe information: {}'.format(str(e)))

    logger.error('Edit recipe does not return a response')
    raise Http404('An unexpected error has occurred')


def view_recipe(requests, recipe_id):
    return None

@csrf_protect
def submit_edit_recipe(request, recipe_id):
    try:
        if request.method == 'POST':
            recipe = Recipe.objects.get(id=recipe_id)

            form_data = request.POST

            recipe.name = form_data.get('name', recipe.name)
            recipe.type = form_data.get('type', recipe.type)
            recipe.short_description = form_data.get('recipe_desc', recipe.short_description)
            recipe.prep_time = form_data.get('prep_time', recipe.prep_time)
            recipe.cook_time = form_data.get('cook_time', recipe.cook_time)
            recipe.calories = form_data.get('calories', recipe.calories)
            recipe.portions = form_data.get('portions', recipe.portions)

            if request.FILES.get('files', None):
                uploaded_file = request.FILES.get('file')

                image_buffer = bytearray()
                for file_chunk in uploaded_file.chunks(2**20):
                    image_buffer += file_chunk

                recipe.picture = image_buffer

            recipe.ingredients.all().delete()
            recipe.instructions.all().delete()

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

            recipe.save()

            return JsonResponse(dict())

        else:
            raise ValueError('Request method not supported for submit edit recipe: {}'.format(request.method))

    except Exception as e:
        logger.exception('Could not submit edits to recipe: {}'.format(str(e)))
        raise Http404('Could not submit edit to recipe')

    logger.error('The edit recipe view does not return a value')
    raise Http404('An unexpected error encountered in submit edit recipe action')


def delete_recipe(requests, recipe_id):
    return None
