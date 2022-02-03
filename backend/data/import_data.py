import csv
import django
import os
import sys


sys.path.append(os.path.abspath('../'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
django.setup()

from api.models import Ingredient


def load_data_to_db(file, model):
    with open(file, 'r', encoding='utf-8') as ingredients_data:
        reader = csv.reader(ingredients_data, delimiter=',')
        for row in reader:
            model.objects.create(
                name=row[0],
                measurement_unit=row[1]
            )


load_data_to_db('ingredients.csv', Ingredient)
