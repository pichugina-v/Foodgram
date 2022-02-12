from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    def shopping_cart_filter(self, queryset, field_name, value):
        return queryset.filter(
            shoppinglist__user=self.request.user.id
        )

    def favorite_filter(self, queryset, field_name, value):
        return queryset.filter(
            is_favorited__user=self.request.user.id
        )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'tags'
        )


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name', )
