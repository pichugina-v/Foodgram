from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .filters import (
    RecipeFilter,
    IngredientFilter
)
from .models import (
    Favorite,
    ShoppingList,
    Tag,
    Ingredient,
    Recipe
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeFullSerializer,
    RecipeCreateSerializer,
    RecipeShortenedSerializer
)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return RecipeCreateSerializer
        return RecipeFullSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(id=pk)
        if request.method == 'GET':
            Favorite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(serializer.data)
        get_object_or_404(Favorite, user=user, recipe=recipe).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['get', 'delete'])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(id=pk)
        if request.method == 'GET':
            ShoppingList.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(serializer.data)
        get_object_or_404(ShoppingList, user=user, recipe=recipe).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
