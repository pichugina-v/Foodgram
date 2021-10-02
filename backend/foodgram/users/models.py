from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=100
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=100
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        unique=True
    )
