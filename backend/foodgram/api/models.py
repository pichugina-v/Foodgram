
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=200
    )
    hex_code = models.CharField(
        verbose_name='Цветовой код',
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор',
        max_length=100,
        unique=True
    )


class Ingrigients(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=50
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingridients = models.ManyToManyField(

    )
    tags = models.ManyToManyField(

    )
    cooking_time = models.PositiveSmallIntegerField(

    )


class IngridientsAmount(models.Model):
    ingridient = models.ForeignKey(
        Ingrigients,
        verbose_name='Ингридиент',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(

    )
