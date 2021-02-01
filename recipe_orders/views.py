
import logging
import io

from django.http import Http404, FileResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import OrderedRecipe

logger = logging.getLogger(__name__)


@login_required()
def show_ordered_recipes(request):
    try:
        if request.method == 'GET':
            recipes = OrderedRecipe.objects.filter(user=request.user)
        else:
            raise ValueError('Unsupported HTTP method to show ordered recipes: {}'.format(request.method))
    except:
        logger.exception('Could not obtain ordered recipes')
        raise Http404()

    return render(
        request,
        'view_ordered_recipes.html',
        context=dict(recipes=recipes)
    )


@login_required()
@csrf_protect
def view_ordered_recipe(request, recipe_id):
    """Render read-only ordered recipe view

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    recipe_id: int
        The backend id of the recipe to view

    Notes
    -----
        This view is to render recipes that have been purchased

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object.
    """
    try:
        if request.method == 'GET':
            # Obtain the recipe from the backend based on the recipe id. Only allow the user to read recipes they have
            # uploaded
            recipe = OrderedRecipe.objects.get(
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
                'ingredients': list(recipe.ordered_ingredients.values_list('description', flat=True)),
                'instructions': list(recipe.ordered_instructions.values_list('description', flat=True)),
            }
            return render(
                request,
                'show_ordered_recipe.html',
                context=dict(
                    recipe=recipe_dict,
                )
            )
        else:
            raise ValueError('Unsupported HTTP method for order view recipe: {}'.format(request.method))
    except Exception as e:
        # When an error occurs send the user an HTTP 404 error
        logger.exception('Could not retrieve recipe information')
        raise Http404('Could not retrieve recipe information: {}'.format(str(e)))

    logger.error('View ordered recipe does not return a response')
    raise Http404('An unexpected error has occurred in viewing ordered recipe')


@login_required()
@csrf_exempt
def download_ordered_recipe_image(request, recipe_id):
    """Download the image of an ordered recipe

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
            recipe = OrderedRecipe.objects.get(id=recipe_id)

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
