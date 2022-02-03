from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    RecipeIngredientAmount,
    Recipe,
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
    list_filter = ('name', 'slug')


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
        'image',
        'text',
        'cooking_time',
        'pub_date'
    )
    inlines = (Recipe_inline,)
    search_fields = ('name', 'tags', 'author')
    list_filter = ('name', 'author')
