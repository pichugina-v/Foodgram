import io

from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import (
    RecipeFilter,
    IngredientFilter
)
from .models import (
    Favorite,
    RecipeIngredientAmount,
    ShoppingList,
    Tag,
    Ingredient,
    Recipe
)
from foodgram.paginators import RecipePagination
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
            methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        if request.method == 'POST':
            Favorite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(serializer.data)
        get_object_or_404(Favorite, user=user, recipe=recipe).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        if request.method == 'POST':
            ShoppingList.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(serializer.data)
        get_object_or_404(ShoppingList, user=user, recipe=recipe).delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'])
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
