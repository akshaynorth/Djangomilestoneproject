
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """Holds Login form information

    The log-in form consists of the username and password fields.
    """
    username = forms.CharField(min_length=8, max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')
        model = User


class RegisterForm(LoginForm):
    """Hols user registration information

    This form inherits from the LoginForm to avoid repetition of fields also required during login
    """
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ('username', 'password', 'email')
        model = User
