from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from mainapp.apps import MainappConfig
from mainapp.views import protected_home, TokenObtainPairView

app_name = MainappConfig.name

urlpatterns = [
    path('', protected_home, name='home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]