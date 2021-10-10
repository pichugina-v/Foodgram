from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet, 
    IngridientViewSet,
    RecipeViewSet
)


router_v1 = routers.DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingridients', IngridientViewSet, basename='ingridients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
