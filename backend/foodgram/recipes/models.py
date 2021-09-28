from django.contrib.auth import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=128,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30,
        blank=True,
        null=True
    )
