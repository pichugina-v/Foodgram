from django.db import models
from django.db.models.fields import CharField
from users.models import User


class Tag(models.Model):
    name = CharField(
        verbose_name='Тег',
        
    )


class Ingrigients(models.Model):



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
