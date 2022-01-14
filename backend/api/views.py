from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Favorite, ShoppingList, Tag, Ingredient, Recipe
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


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

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