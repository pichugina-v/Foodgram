import io
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import mixins, status
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
from .utils import collect_ingredients


FAVORITE_ERRORS = {
    'exists': ('Рецепт уже добавлен '
               'в Ваш список избранного'),
    'does_not_exist': ('В Вашем списке избранного '
                       'нет выбранного рецепта')
}
SHOPPING_LIST_ERRORS = {
    'exists': ('Рецепт уже добавлен '
               'в Ваш список покупок'),
    'does_not_exist': ('В Вашем списке покупок '
                       'нет выбранного рецепта')
}
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

    def add_delete_recipe(self, request, pk, model, errors):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        selected_recipe = model.objects.filter(
            user=user,
            recipe=recipe
        )
        if request.method == 'POST':
            if selected_recipe.exists():
                return Response(
                    {"errors": errors.get('exists')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            model.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = RecipeShortenedSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if selected_recipe.count() == 0:
            return Response(
                {"errors": errors.get('does_not_exist')},
                status=status.HTTP_400_BAD_REQUEST
            )
        selected_recipe.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_delete_recipe(
            request, 
            pk,
            Favorite,
            FAVORITE_ERRORS
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_delete_recipe(
            request,
            pk,
            ShoppingList,
            SHOPPING_LIST_ERRORS
        )

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = collect_ingredients(request)
        buffer = io.BytesIO()
        pdfmetrics.registerFont(
            TTFont('DejaVuSans', 'DejaVuSans.ttf')
        )
        pdf_object = canvas.Canvas(buffer)
        pdf_object.setFont('DejaVuSans', 14)
        height = 800
        for ingredient in ingredients:
            pdf_object.drawString(
                1,
                height,
                (f'{ingredient.get("ingredients__name")} - '
                 f'{ingredient.get("ingredients__measurement_unit")} '
                 f'{ingredient.get("total_amount")}')
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
