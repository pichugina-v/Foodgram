from rest_framework import serializers

from users.serializers import UserSerializer
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    Tag,
    ShoppingList
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeShortenedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientAmount
        fields = (
            'id',
            'amount'
        )


class RecipeFullSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = UserSerializer(
        read_only=True
    )
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            # 'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = obj.recipeingredientamount_set.all()
        return RecipeIngredientAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if (user.id is not None and Favorite.objects.filter(
                user=user, recipe=obj).exists()):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if (user.id is not None and ShoppingList.objects.filter(
                user=user, recipe=obj
           ).exists()):
            return True
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    ingredients = RecipeIngredientCreateSerializer(
        source='recipeingredientamount_set',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
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
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            # 'image',
            'text',
            'cooking_time'
        )

    def set_tags_and_ingredients(self, tags, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredientAmount.objects.create(
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount'],
                recipe=recipe
            )
        recipe.tags.set(tags)
        return recipe

    def create(self, validated_data):
        ingredients_data = validated_data.pop(
            'recipeingredientamount_set'
        )
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.set_tags_and_ingredients(
            tags_data,
            ingredients_data,
            recipe
        )

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop(
            'recipeingredientamount_set'
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
        RecipeIngredientAmount.objects.filter(recipe=instance).delete()
        return self.set_tags_and_ingredients(
            tags_data,
            ingredients_data,
            instance
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if ShoppingList.objects.filter(user=user, recipe=obj).exists():
            return True
        return False
