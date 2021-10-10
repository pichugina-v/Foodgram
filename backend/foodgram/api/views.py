from rest_framework.viewsets import ModelViewSet

from .models import Tag, Ingridient, Recipe
from .serializers import (
    TagSerializer,
    IngridientSerializer,
    RecipeSerializer
)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(ModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
