from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet,
    IngridientViewSet,
    RecipeViewSet
)


router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingridients', IngridientViewSet, basename='ingridients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('',
         include(router.urls))
]
