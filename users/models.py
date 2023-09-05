from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser, models.Model):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name='телефон', null=True, blank=True)
    country = models.CharField(max_length=30, verbose_name='страна', null=True, blank=True)

    is_email_verified = models.BooleanField(default=False, verbose_name='статус верификации email')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
