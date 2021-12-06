from django.contrib import admin

from .models import (
    Tag,
    Ingridient,
    IngridientAmount,
    Recipe,
)


class Recipe_inline(admin.TabularInline):
    model = IngridientAmount
    extra = 4


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
        'hex_code', 'slug'
    )
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
        'measurement_unit'
    )
    inlines = (Recipe_inline,)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(IngridientAmount)
class IngridientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ingridient',
        'recipe', 'amount'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author',
        'name', 'image',
        'text', 'cooking_time',
        'pub_date'
    )
    inlines = (Recipe_inline,)
    search_fields = ('name', 'tags', 'author')
    list_filter = ('name', 'author')
