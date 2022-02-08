from .models import (
    Recipe,
    RecipeIngredientAmount
)


def collect_shopping_cart(request):
    result = {}
    recipes_in_user_shopping_list = Recipe.objects.filter(
        shoppinglist__user=request.user
    )
    for recipe in recipes_in_user_shopping_list:
        ingredients = RecipeIngredientAmount.objects.filter(
            recipe=recipe
        )
        for ingredient in ingredients:
            name, unit, amount = (
                ingredient.ingredient.name,
                ingredient.ingredient.measurement_unit,
                ingredient.amount
            )
            if name in result.keys():
                result[name]['amount'] += amount
            else:
                result[name] = {
                    'amount': amount,
                    'unit': unit
                }
    return result
