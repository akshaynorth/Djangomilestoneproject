from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect


def recipe1(request):
    """Display the first recipe of the site

    This is to render a sample recipe that could be uploaded to the site to encourage users to buy recipes.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'recipe-page-1.html')


def recipe2(request):
    """Display the second of the site

    This is to render a sample recipe that could be uploaded to the site to encourage users to buy recipes.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'recipe-page-2.html')


def recipe3(request):
    """Display the third recipe of the site

    This is to render a sample recipe that could be uploaded to the site to encourage users to buy recipes.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'recipe-page-3.html')


def recipe4(request):
    """Display the fourth recipe of the site

    This is to render a sample recipe that could be uploaded to the site to encourage users to buy recipes.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'recipe-page-4.html')


def recipe5(request):
    """Display the fifth recipe of the site

    This is to render a sample recipe that could be uploaded to the site to encourage users to buy recipes.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'recipe-page-5.html')


@login_required()
@csrf_protect
def submit_recipe(request):
    """Display the recipe submission page

    Users are required to be registered and logged in before they can submit a recipe

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'submit-recipe.html')


@login_required()
@csrf_protect
def search(request):
    """Display the recipe search input form

    Users are required to be registered and logged in before they can search for a recipe

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    return render(request,
                  'browse-recipes.html')
