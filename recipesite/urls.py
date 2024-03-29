"""recipesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('', include('recipe.urls')),
    path('login/', include('login_app.urls')),
    path('pages/', include('pages.urls')),
    path('recipe/', include('recipe.urls')),
    path('recipe_cart/', include('recipe_cart.urls')),
    path('recipe_pay/', include('recipe_pay.urls')),
    path('recipe_orders/', include('recipe_orders.urls')),
    re_path(r'^create-checkout-session$', include('recipe_pay.urls')),
    path('admin/', admin.site.urls)
]
