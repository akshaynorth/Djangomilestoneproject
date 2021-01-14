
from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^login_form/$', views.user_login_form, name='login_form'),
    re_path('^user_login/$', views.user_login, name='login'),
    re_path('^user_logout/$', views.user_logout, name='logout'),
    re_path('^register_form/$', views.user_register_form, name='register_form'),
    re_path('^register/$', views.user_register, name='register')
]
