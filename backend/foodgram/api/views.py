from rest_framework.viewsets import ModelViewSet

from .models import Tag, Ingridient, Recipe
from .serializers import (
    TagSerializer,
    IngridientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer
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

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return RecipeCreateSerializer
        return RecipeSerializer
