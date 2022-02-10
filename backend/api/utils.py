from django.db.models import Sum

from .models import (
    Recipe
)


def collect_ingredients(request):
    ingredients = Recipe.objects.filter(
        shoppinglist__user=request.user
    ).values(
        'ingredients__name',
        'ingredients__measurement_unit',
        'ingredient_in_recipe__amount'
    ).annotate(
        total_amount=Sum(
            'ingredient_in_recipe__amount'
        )
    )
    return ingredients
