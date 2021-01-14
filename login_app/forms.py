
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(min_length=8, max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')
        model = User


class RegisterForm(LoginForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ('username', 'password', 'email')
        model = User
