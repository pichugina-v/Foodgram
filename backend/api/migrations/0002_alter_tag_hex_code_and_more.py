# Generated by Django 4.0.1 on 2022-02-09 14:30

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='hex_code',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None, unique=True, verbose_name='Цветовой код'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_recipe_in_user_favorite'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_in_recipe'),
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_recipe_in_user_list'),
        ),
    ]
