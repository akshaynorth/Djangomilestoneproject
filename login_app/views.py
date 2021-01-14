from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
from .forms import LoginForm, RegisterForm


def user_login_form(request):

    login_form = LoginForm()

    return render(
        request,
        'login.html',
        context=dict(login_form=login_form)
    )


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # Obtained details for authentication from:
            #   https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.login
            user = authenticate(request, login_form.username, login_form.password)
            if user is not None:
                login(request, user)

                return HttpResponseRedirect(reverse('index'))

    else:
        login_form = LoginForm()

    return render(
        request,
        'login.html',
        context=dict(login_form=login_form)
    )


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_register_form(request):
    if request.method == 'GET':

        register_form = RegisterForm()

        return render(
            request,
            'register.html',
            context=dict(register_form=register_form)
        )
    else:
        return HttpResponseRedirect(reverse('index'))


def user_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            User.objects.create_user(
                username=register_form.cleaned_data['username'],
                email=register_form.cleaned_data['email'],
                password=register_form.cleaned_data['password']
            )
        else:
            return render(
                request,
                'register.html',
                context=dict(register_form=register_form)
            )
    else:
        return HttpResponseRedirect(reverse('index'))
