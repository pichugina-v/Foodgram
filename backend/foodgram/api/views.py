from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Favorite, Tag, Ingridient, Recipe
from .serializers import (
    TagSerializer,
    IngridientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    FavoriteRecipeSerializer
)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(ModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=True,
            methods=['get', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(id=pk)
        if request.method == 'get':
            Favorite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data)
        get_object_or_404(Recipe, user=user, recipe=recipe).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)