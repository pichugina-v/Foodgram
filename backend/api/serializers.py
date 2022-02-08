from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    Tag,
    ShoppingList,
    COOKING_TIME_AMOUNT_VALIDATION
)


DUPLICATE_INGREDIENTS = ('Ингредиенты в рецепте '
                         'не должны дублироваться')
INGREDIENTS_NOT_NULL = 'Укажите минимум один игредиент'
TAGS_NOT_NULL = 'Укажите минимум один тег'


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

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError(
                COOKING_TIME_AMOUNT_VALIDATION
            )
        return amount


class RecipeFullSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = UserSerializer(
        read_only=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True
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
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = obj.ingredient_in_recipe.all()
        return RecipeIngredientAmountSerializer(
            ingredients, many=True
        ).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if (user.id is not None and Favorite.objects.filter(
                user=user, recipe=obj
        ).exists()):
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
        source='ingredient_in_recipe',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True
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
            'image',
            'text',
            'cooking_time'
        )

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                INGREDIENTS_NOT_NULL
            )
        ingredients_names = [
            ingredient['ingredient'] for ingredient in ingredients
        ]
        if len(ingredients_names) > len(set(ingredients_names)):
            raise serializers.ValidationError(
                DUPLICATE_INGREDIENTS
            )
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                TAGS_NOT_NULL
            )
        return tags

    def set_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredientAmount.objects.create(
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount'],
                recipe=recipe
            )
        return recipe

    def check_value_exists(self, obj, model_name):
        user = self.context['request'].user
        if (user.id is not None and model_name.objects.filter(
            user=user, recipe=obj
        ).exists()):
            return True
        return False

    def create(self, validated_data):
        author = self.context['request'].user
        ingredients_data = validated_data.pop(
            'ingredient_in_recipe'
        )
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data,
            author=author
        )
        recipe.tags.set(tags_data)
        return self.set_ingredients(
            ingredients_data,
            recipe
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.author = validated_data.get('author', instance.author)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        if self.initial_data.get('tags'):
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.set(tags_data)
        if self.initial_data.get('ingredients'):
            ingredients_data = validated_data.pop(
                'ingredient_in_recipe'
            )
            instance.ingredients.clear()
            self.set_ingredients(
                ingredients_data,
                instance
            )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        return self.check_value_exists(
            obj, Favorite
        )

    def get_is_in_shopping_cart(self, obj):
        return self.check_value_exists(
            obj, ShoppingList
        )
