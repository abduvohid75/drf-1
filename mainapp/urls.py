from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from mainapp.apps import MainappConfig
from mainapp.views import home
from rest_framework import routers

app_name = MainappConfig.name

urlpatterns = [
    path('', home, name='home'),
]
