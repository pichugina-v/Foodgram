# Generated by Django 4.0.1 on 2022-02-06 10:54

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[api.models.validate_amount], verbose_name='Количество'),
        ),
    ]
