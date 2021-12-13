import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import UserSerializer
from .models import Favorite, Tag, Ingridient, IngridientAmount, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = ('__all__')


class IngridientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
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


class RecipeIngridientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingridient',
        queryset=Ingridient.objects.all()
    )
    amount = serializers.IntegerField()

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
    ingridients = serializers.SerializerMethodField()
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

    def get_ingridients(self, obj):
        ingridients = obj.ingridientamount_set.all()
        return IngridientAmountSerializer(ingridients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        return True


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    ingridients = RecipeIngridientCreateSerializer(
        source='ingridientamount_set',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingridients',
            'name',
            # 'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingridients_data = validated_data.pop(
            'ingridientamount_set'
        )
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingridient in ingridients_data:
            IngridientAmount.objects.create(
                ingridient=ingridient['ingridient'],
                amount=ingridient['amount'],
                recipe=recipe
            )
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingridients_data = validated_data.pop(
            'ingridientamount_set'
        )
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.author = validated_data.get('author', instance.author)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        IngridientAmount.objects.filter(recipe=instance).delete()
        for ingridient in ingridients_data:
            ingridient = IngridientAmount.objects.create(
                ingridient=ingridient['ingridient'],
                amount=ingridient['amount'],
                recipe=instance
            )
        instance.tags.set(tags_data)
        return instance
