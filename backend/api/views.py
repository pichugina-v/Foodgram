import io

from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from foodgram.paginators import RecipePagination
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
from .permissions import (
    IsAuthorOrAuthenticatedOrReadOnly
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeFullSerializer,
    RecipeCreateSerializer,
    RecipeShortenedSerializer
)
from .utils import collect_shopping_cart


RECIPE_ALREADY_IN_FAVORITE = ('Рецепт уже добавлен '
                              'в Ваш список избранного')
RECIPE_ALREADY_IN_SHOPPING_LIST = ('Рецепт уже добавлен '
                                   'в Ваш список покупок')
RECIPE_IS_NOT_IN_FAVORITE = ('В Вашем списке избранного '
                             'нет выбранного рецепта')
RECIPE_IS_NOT_IN_SHOPPING_LIST = ('В Вашем списке покупок '
                                  'нет выбранного рецепта')
PDF_FILENAME = 'Список игредиентов.pdf'


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
    permission_classes = [IsAuthorOrAuthenticatedOrReadOnly]
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeFullSerializer
        return RecipeCreateSerializer

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
        if request.method == 'POST':
            if favorite_recipe.exists():
                return Response(
                    {"errors": RECIPE_ALREADY_IN_FAVORITE},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
                {"errors": RECIPE_IS_NOT_IN_FAVORITE},
                status=status.HTTP_400_BAD_REQUEST
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
        if request.method == 'POST':
            if purchase.exists():
                return Response(
                    {"errors": RECIPE_ALREADY_IN_SHOPPING_LIST},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
                {"errors": RECIPE_IS_NOT_IN_SHOPPING_LIST},
                status=status.HTTP_400_BAD_REQUEST
            )
        purchase.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart = collect_shopping_cart(request)
        buffer = io.BytesIO()
        pdfmetrics.registerFont(
            TTFont('DejaVuSans', 'DejaVuSans.ttf')
        )
        pdf_object = canvas.Canvas(buffer)
        pdf_object.setFont('DejaVuSans', 14)
        height = 800
        for name in shopping_cart.keys():
            pdf_object.drawString(
                1,
                height,
                (f'{name} - {shopping_cart[name]["amount"]} '
                 f'{shopping_cart[name]["unit"]}')
            )
            height -= 20
        pdf_object.showPage()
        pdf_object.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=PDF_FILENAME
        )
