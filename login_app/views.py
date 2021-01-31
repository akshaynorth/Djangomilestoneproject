import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
from .forms import LoginForm, RegisterForm

logger = logging.getLogger(__name__)


def user_login_form(request):
    """Displays log-in page for authentication

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object
    """
    login_form = LoginForm()

    return render(
        request,
        'login.html',
        context=dict(login_form=login_form)
    )


def user_login(request):
    """Authenticate the user after submitting the log-in page

    The login form is validated by the Django LoginForm. Errors are added for display to the user screen. This function
    uses the built-in Django authentication framework to authenticate users. See:
    https://docs.djangoproject.com/en/3.1/topics/auth/ for details

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. When there are errors, the log in page is rendered
        again with the errors. After successful log-in, the page that required authentication is rendered.
    """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # Obtained details for authentication from:
            #   https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.login
            try:
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )

                if user is not None:
                    login(request, user)

                    return HttpResponseRedirect(reverse('index'))

            except:
                logger.exception('Could not authenticate user')

            login_form.add_error('username', 'Could not authenticate user: {}'.format(
                login_form.cleaned_data['username'])
            )

    else:
        login_form = LoginForm()

    return render(
        request,
        'login.html',
        context=dict(login_form=login_form)
    )


def user_logout(request):
    """Perform the logout of the authenticated user

    This function uses the built-in Django authentication mechanism to logout users. See:
    https://docs.djangoproject.com/en/3.1/topics/auth/ for details.

    Upon successful login, the user is sent to the home page.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_register_form(request):
    """Render the user registration form

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the custom-built registration form
    """
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
    """Registers a user to the site

    Users are maintained in the backend database. The built-in Django authentication framework is used to manage the
    encryption of the password and storage of users profiles. Upon successful log-in, the user is forwarded to the
    home page. The user is forwarded to the user registration form is field validation fails.

    Parameters
    ----------
    request: django.http.HttpRequest
        Django HTTP request object with request information submitted by web browser client

    Returns
    -------
    django.http.HttpResponse
        The rendered HTML page in a Django HttpResponse object. This will be the home page of the site.
    """
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            User.objects.create_user(
                username=register_form.cleaned_data['username'],
                email=register_form.cleaned_data['email'],
                password=register_form.cleaned_data['password']
            )

            return HttpResponseRedirect(reverse('index'))
        else:
            return render(
                request,
                'register.html',
                context=dict(register_form=register_form)
            )
    else:
        return HttpResponseRedirect(reverse('index'))
