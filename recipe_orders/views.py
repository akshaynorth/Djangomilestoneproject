
import logging

from django.http import Http404
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .models import OrderedRecipe

logger = logging.getLogger(__name__)


@login_required()
def show_ordered_recipes(request):
    recipes = None
    # try:
    #     if request.method == 'GET':
    #         recipes = OrderedRecipe.objects.filter(user=request.user)
    #     else:
    #         raise ValueError('Unsupported HTTP method to show ordered recipes: {}'.format(request.method))
    # except:
    #     logger.exception('Could not obtain ordered recipes')
    #     raise Http404()

    return render(
        'view_ordered_recipes.html',
        context=dict(recipes=recipes)
    )
