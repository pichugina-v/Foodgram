from django.db.models.fields import IntegerField
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Tag, Ingridient, IngridientAmount, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = ('__all__')


class IngridientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingridient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingridient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingridient.measurement_unit'
    )

    class Meta:
        model = IngridientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngridientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingridient.objects.all()
    )
    amount = IntegerField()

    class Meta:
        model = IngridientAmount
        fields = (
            'id',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = UserSerializer(
        read_only=True
    )
    ingridients = IngridientAmountSerializer(
        source='ingridientamount_set',
        read_only=True,
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingridients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return True

    def get_is_in_shopping_cart(self, obj):
        return True


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #ingridients = IngridientRecipeCreateSerializer(
    #    many=True
    #)
    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            #'ingridients',
            'name',
            #'image',
            'text',
            'cooking_time'
        )
