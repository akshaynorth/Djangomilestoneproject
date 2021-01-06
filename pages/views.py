from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(requests):
    return render(requests,
                  'index.html')


def recipe1(requests):
    return render(requests,
                  'recipe-page-1.html')


def recipe2(requests):
    return render(requests,
                  'recipe-page-2.html')


def recipe3(requests):
    return render(requests,
                  'recipe-page-3.html')


def recipe4(requests):
    return render(requests,
                  'recipe-page-4.html')


def recipe5(requests):
    return render(requests,
                  'recipe-page-5.html')


def submit_recipe(requests):
    return render(requests,
                  'submit-recipe.html')


def search(requests):
    return render(requests,
                  'browse-recipes.html')
