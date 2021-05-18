from django.shortcuts import render

# Create your views here.

import json

import logging
import datetime
import io

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, FileResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q, Count
from .models import Recipe, RecipeIngredient, RecipeInstruction

logger = logging.getLogger(__name__)


def index(request):
    """Renders the site home page

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    recipes = []
    try:
        if request.method == 'GET':
            # Limit the most recently added recipes up to 10
            # Present the user with a list of recipes that have been recently added to give an indication of
            # activity
            if Recipe.objects.first():
                recipes = list(Recipe.objects.all().order_by('creation_time')[:10])
        else:
            raise ValueError('HTTP method not supported for home pages: {}'.format(request.method))
    except Exception as e:
        logger.exception('Could not render home page')
        Http404('Could not render home page: {}'.format(str(e)))

    return render(request,
                  'index.html',
                  context=dict(recipe_list=recipes)
                  )


@login_required()
@csrf_protect
def create(request):
    """Create a new recipe in the backend

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'POST':
            form_data = request.POST

            # Create a new recipe in the backend. Use the submitted create recipe form data
            recipe = Recipe.objects.create(
                creation_time=datetime.datetime.now(),
                name=form_data.get('name', ''),
                type=form_data.get('type', ''),
                short_description=form_data.get('recipe_desc', ''),
                prep_time=form_data.get('prep_time', ''),
                cook_time=form_data.get('cook_time', ''),
                calories=form_data.get('calories', ''),
                portions=form_data.get('portions', ''),
                # Let the absence of a price fail the create
                price=form_data.get('price'),
                user=request.user
            )

            # The recipe picture is optional. If provided, obtain all the image data and store it as recipe
            # picture
            if request.FILES.get('file', None):
                uploaded_file = request.FILES.get('file')

                # Upload file in 1 MB chunks
                image_buffer = bytearray()
                for file_chunk in uploaded_file.chunks(2**20):
                    image_buffer += file_chunk

                recipe.picture = image_buffer

            recipe.save()

            # Add the ingredients provided via the request
            for ingredient in json.loads(form_data.get('ingredients', '[]')):
                RecipeIngredient.objects.create(
                    description=ingredient,
                    recipe=recipe
                )

            # Add the instructions provided via the request
            for instruction in json.loads(form_data.get('instructions', '[]')):
                RecipeInstruction.objects.create(
                    description=instruction,
                    recipe=recipe
                )
        else:
            # Do not allow someone to submit an non-POST request to create recipes
            raise ValueError('Invalid HTTP method for recipe create')

    except Exception as e:
        # When an error occurs return a user an HTTP 404 error page
        logger.exception('Could not create recipe')
        return JsonResponse(
            dict(error=str(e)),
            status=404
        )

    return JsonResponse(
        dict()
    )


@login_required()
@csrf_protect
def search_recipe(request):
    """Serve the search for the recipe

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Notes
    -----
        Some fields in the search form are optional. The search needs to be further restricted the more values are
        provided by a user. A user should type in a category and if none is found, it is assumed a search for all
        available recipes. The search recipe result set is to be edited by the user (e.g. Edit, Delete). For this
        reason only the recipes the user has registered are shown.

        The search for text within the ingredients and instructions is a substring search. As there is a need for a
        variable and unpredictable set of query parameters, this function relies on *args and **kwargs that can be
        passed to the Django ORM.

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'POST':
            form_data = request.POST

            query_dict = dict()

            recipe_type = form_data.get('type', None)
            # When the user selects a recipe category, restrict the search for that recipe type by adding it
            # to the Django ORM filter function call parameter list
            if recipe_type and recipe_type.upper() != 'ALL':
                query_dict.update(
                    dict(
                      type=recipe_type
                    )
                )

            ingredient_list = json.loads(form_data.get('ingredient_list', '[]'))

            ingredient_query_args = None

            if ingredient_list:
                ingredient_search_type = form_data.get('ingredient_search_type', None)

                for ingredient in ingredient_list:
                    if ingredient_query_args:
                        ingredient_query_args = (ingredient_query_args[0] |
                                                 Q(ingredient__description__icontains=ingredient), )

                    else:
                        ingredient_query_args = (
                            Q(ingredient__description__icontains=ingredient),
                        )

                # Finding recipes that contain all the ingredients passed in the search was
                # challenging with Django ORM. The closest solution was to find the ingredients matching
                # the ingredient text search and counting the number of ingredients being a match. The count of
                # ingredients found is assumed to be equal to the number of searched ingredients. This
                # assumption presumes each ingredient is stored in a separate row within the recipe ingredient
                # table.

                if ingredient_search_type and ingredient_search_type.upper() != 'ALL':
                    ingredient_list_len = 1
                else:
                    ingredient_list_len = len(ingredient_list)

                recipes_with_ings_qs = Recipe.objects.filter(
                    *ingredient_query_args
                ).annotate(
                    num_ingredient=Count('ingredient')
                ).filter(num_ingredient__gte=ingredient_list_len)

                # Add the recipes found with the ingredients to the filter
                if recipes_with_ings_qs:
                    query_dict.update(
                        dict(id__in=recipes_with_ings_qs)
                    )
                else:
                    # Add a bogus ID that will result in no recipes found as no recipes were found matching all the
                    # ingredients
                    query_dict.update(
                        dict(id__in=[-1])
                    )

            # Restrict search results to recipes the user owns
            query_dict.update(
                user=request.user
            )

            recipes = Recipe.objects.filter(**query_dict)

            return render(
                request,
                'browse-recipes.html',
                context=dict(recipe_list=recipes)
            )

        else:
            raise ValueError('Only HTTP POST supported for search recipes')
    except Exception as e:
        # When an error occurs send the user an HTTP 404 error page
        logger.exception('Could not complete search for recipe')
        raise Http404('Could not search recipe: {}'.format(str(e)))

    raise Http404('Unexpected error has occurred while searching for recipe')


@login_required()
@csrf_exempt
def download_recipe_image(request, recipe_id):
    """Download the image of a recipe

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The backend id of the recipe to download a picture form

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'GET':
            # Obtain the image from the database
            recipe = Recipe.objects.get(id=recipe_id)

            image_data = recipe.picture

            # Send a file response with the binary data to the web client
            return FileResponse(
                io.BytesIO(image_data)
            )
        else:
            raise ValueError('HTTP method POST not supported for image download')

    except Exception as e:
        # When an error occurs, send the user an HTTP 404 errors. In this case, image GET operation will result in no
        # image displayed
        logger.exception('Could not download recipe image')
        raise Http404('Could not download image for recipe: {}'.format(e))

    raise Http404('Unexpected error has occurred')


@login_required()
@csrf_protect
def edit_recipe(request, recipe_id):
    """Render the edit recipe page

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The backend id of the recipe to edit

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'GET':
            # Obtain the recipe backend information based on the recipe id
            recipe = Recipe.objects.get(id=recipe_id)

            recipe_dict = {
                'id': recipe.id,
                'name': recipe.name,
                'type': recipe.type,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'calories': recipe.calories,
                'portions': recipe.portions,
                'price': recipe.price,
                'short_description': recipe.short_description,
                'ingredients': list(recipe.ingredients.values_list('description', flat=True)),
                'instructions': list(recipe.instructions.values_list('description', flat=True)),
            }

            # The recipe type is not stored on the database but is required for the selection of the category
            # pass the recipe types to satisfy the distinction of recipe categories
            # The recipe object is provided to allow the form to display the pre-filled values of the recipe stored in
            # the backend
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
        # When an error occurs, send the user an HTTP 404 error
        logger.exception('Could not retrieve recipe information')
        raise Http404('Could not retrieve recipe information: {}'.format(str(e)))

    logger.error('Edit recipe does not return a response')
    raise Http404('An unexpected error has occurred')


@login_required()
@csrf_protect
def view_recipe(request, recipe_id):
    """Render read-only recipe view

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The backend id of the recipe to view

    Notes
    -----
        This view is to render recipes to the user that have access to see for the purpose of reviewing user-uploaded
        recipe information. This is not meant for all users to see recipes they have not uploaded without purchase.

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'GET':
            # Obtain the recipe from the backend based on the recipe id. Only allow the user to read recipes they have
            # uploaded
            recipe = Recipe.objects.get(
                user=request.user,
                id=recipe_id
            )

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
                'recipe-view.html',
                context=dict(
                    recipe=recipe_dict,
                )
            )
        else:
            raise ValueError('Unsupported HTTP method for edit recipe: {}'.format(request.method))
    except Exception as e:
        # When an error occurs send the user an HTTP 404 error
        logger.exception('Could not retrieve recipe information')
        raise Http404('Could not retrieve recipe information: {}'.format(str(e)))

    logger.error('Edit recipe does not return a response')
    raise Http404('An unexpected error has occurred in viewing recipe')


@login_required()
@csrf_protect
def submit_edit_recipe(request, recipe_id):
    """Stores edited recipe information

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The backend id of the recipe to view

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'POST':
            # Obtain the recipe from the backend based on the recipe id
            recipe = Recipe.objects.get(id=recipe_id)

            form_data = request.POST

            recipe.name = form_data.get('name', recipe.name)
            recipe.type = form_data.get('type', recipe.type)
            recipe.short_description = form_data.get('recipe_desc', recipe.short_description)
            recipe.prep_time = form_data.get('prep_time', recipe.prep_time)
            recipe.cook_time = form_data.get('cook_time', recipe.cook_time)
            recipe.calories = form_data.get('calories', recipe.calories)
            recipe.portions = form_data.get('portions', recipe.portions)
            recipe.price = form_data.get('price', recipe.price)

            # If a new picture is provided, then obtain its binary information
            if request.FILES.get('file', None):
                uploaded_file = request.FILES.get('file')

                image_buffer = bytearray()
                for file_chunk in uploaded_file.chunks(2**20):
                    image_buffer += file_chunk

                recipe.picture = image_buffer

            # Recreate the ingredients and instruction such that the result is a match of the ones edited by the
            # user
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
        # When an error occurs, send an HTTP 404 error to the user
        logger.exception('Could not submit edits to recipe: {}'.format(str(e)))
        raise Http404('Could not submit edit to recipe')

    logger.error('The edit recipe view does not return a value')
    raise Http404('An unexpected error encountered in submit edit recipe action')


@login_required()
@csrf_protect
def delete_recipe(request, recipe_id):
    """Deletes a recipe from the backend

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The backend id of the recipe to view

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'POST':
            # Delete the recipe in the backend based on the provided recipe id
            # When a non-existent recipe id is provided, this call will fail and the user will be sent an error
            Recipe.objects.get(id=recipe_id).delete()

            return JsonResponse(dict())
        else:
            raise ValueError('Request method not supported for delete recipe: {}'.format(request.method))

    except Exception as e:
        # When an error occurs, send the user an HTTP 404 error
        logger.exception('Could not delete recipe')
        raise Http404()

    logger.error('The delete recipe view does not return a value')

    raise Http404('An unexpected error encountered in delete recipe action')
