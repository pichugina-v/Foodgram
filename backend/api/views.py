import io

from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import (
    RecipeFilter,
    IngredientFilter
)
from foodgram.paginators import RecipePagination
from .models import (
    Favorite,
    RecipeIngredientAmount,
    ShoppingList,
    Tag,
    Ingredient,
    Recipe
)
from .permissions import (
    IsAuthorOrReadOnly
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
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeFullSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        favorite_recipe = Favorite.objects.filter(
            user=user,
            recipe=recipe
        )
        if favorite_recipe.exists():
            return Response(
                {"errors": "Рецепт уже добавлен в избранное"}
            )
        if request.method == 'POST':
            Favorite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if favorite_recipe.count() == 0:
            return Response(
                {"errors": "В Вашем списке избранного нет выбранного рецепта"}
            )
        favorite_recipe.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        purchase = ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        )
        if purchase.exists():
            return Response(
                {"errors": "Рецепт уже добавлен в список покупок"}
            )
        if request.method == 'POST':
            ShoppingList.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if purchase.count() == 0:
            return Response(
                {"errors": "В Вашем списке покупок нет выбранного рецепта"}
            )
        purchase.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        result = {}
        recipes_in_user_shopping_list = Recipe.objects.filter(
            shoppinglist__user=request.user
        )
        for recipe in recipes_in_user_shopping_list:
            ingredients = RecipeIngredientAmount.objects.filter(
                recipe=recipe
            )
            for ingredient in ingredients:
                name, unit, amount = (
                    ingredient.ingredient.name,
                    ingredient.ingredient.measurement_unit,
                    ingredient.amount
                )
                if name in result.keys():
                    result[name]['amount'] += amount
                else:
                    result[name] = {
                        'amount': amount,
                        'unit': unit
                    }
        buffer = io.BytesIO()
        pdfmetrics.registerFont(
            TTFont('DejaVuSans', 'DejaVuSans.ttf')
        )
        pdf_object = canvas.Canvas(buffer)
        pdf_object.setFont('DejaVuSans', 14)
        height = 800
        for name in result.keys():
            pdf_object.drawString(
                1,
                height,
                (f'{name} - {result[name]["amount"]} '
                 f'{result[name]["unit"]}')
            )
            height -= 20
        pdf_object.showPage()
        pdf_object.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='Список игредиентов.pdf'
        )
