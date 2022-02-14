from django.db.models import Sum

from .models import Recipe


def collect_ingredients(request):
    return Recipe.objects.filter(
        shoppinglist__user=request.user
    ).values(
        'ingredients__name',
        'ingredients__measurement_unit'
    ).annotate(
        total_amount=Sum(
            'ingredients__amount'
        )
    )
