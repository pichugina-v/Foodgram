from colorfield.fields import ColorField

from django.db import models
from django.db.models.fields.related import ForeignKey

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=200
    )
    hex_code = ColorField(
        verbose_name='Цветовой код',
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['id']

    def __str__(self):
        return self.name
        # return (f'{self.name}, '
        #         f'{self.measurement_unit}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return (f'{self.name}, '
                f'{self.pub_date}, '
                f'{self.text[:15]}, '
                f'{self.author}')


class RecipeIngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингридиент',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингридиентов в рецепте'
        verbose_name_plural = 'Количество ингридиентов в рецепте'

    def __str__(self):
        return (f'{self.ingredient} '
                f'{self.amount} в {self.recipe}')


class ShoppingList(models.Model):
    user = ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipe = ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.recipe} в списке '
                f'покупок пользователя {self.user}')


class Favorite(models.Model):
    user = ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipe = ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список избранных рецептов'
        verbose_name_plural = 'Списки избранных рецептов'

    def __str__(self):
        return (f'{self.recipe} в списке '
                f'избранного пользователя {self.user}')
