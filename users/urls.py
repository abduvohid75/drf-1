from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, send_verification_email, verify_email, suc_pass, change_password

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='user_reg'),
    path('profile', ProfileView.as_view(template_name='users/profile.html'), name='profile'),
    path('password', PasswordChangeView.as_view(template_name='users/password.html', success_url = reverse_lazy('users:suc_pass')), name='password'),
    path('password/done', suc_pass, name='suc_pass'),
    path('password/generate', change_password, name='generate_password'),
    path('verification', send_verification_email, name='verify'),
    path('verification/verify/<str:uid64>/<str:token>', verify_email, name='verify_email'),
]
