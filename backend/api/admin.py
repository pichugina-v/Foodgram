from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    RecipeIngredientAmount,
    Recipe,
    ShoppingList,
    Favorite
)


class Recipe_inline(admin.TabularInline):
    model = RecipeIngredientAmount
    extra = 4


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'hex_code',
        'slug'
    )
    search_fields = ('name', 'slug')
    list_filter = ('slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    inlines = (Recipe_inline,)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(RecipeIngredientAmount)
class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'get_recipe_favorited'
    )
    readonly_fields = ('get_recipe_favorited', )
    inlines = (Recipe_inline,)
    search_fields = ('name', 'tags', 'author')
    list_filter = ('tags', 'pub_date')

    def get_recipe_favorited(self, obj):
        return obj.is_favorited.count()

    get_recipe_favorited.short_description = ('Количество добавлений '
                                              'рецепта в избранное')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    search_fields = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    search_fields = ('user', 'recipe')
