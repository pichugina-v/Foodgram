import csv

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            './data/ingredients.csv', 'r', encoding='utf-8'
        ) as ingredients_data:
            reader = csv.reader(ingredients_data)
            for row in reader:
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
