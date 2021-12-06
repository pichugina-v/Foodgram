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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'Username: {self.username}, '
                f'адрес электронной почты: {self.email}, ')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (f'Подписчик: {self.user.username}, '
                f'автор: {self.author.username}')
