import csv
import django
import os
import sys


sys.path.append(os.path.abspath('../'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
django.setup()


def main():
    from api.models import Ingredient
    with open(
        'ingredients.csv', 'r', encoding='utf-8'
    ) as ingredients_data:
        reader = csv.reader(ingredients_data)
        for row in reader:
            Ingredient.objects.create(
                name=row[0],
                measurement_unit=row[1]
            )


if __name__ == '__main__':
    main()
