from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.serializers.nested_serializers import RecipeShortenedSerializer
from api.models import Recipe
from .models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.id is not None and Follow.objects.filter(
            user=self.context['request'].user, author=obj
        ).exists())


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit', None
        )
        recipes = Recipe.objects.filter(
            author=obj
        )
        if recipes_limit is not None:
            return RecipeShortenedSerializer(
                recipes[:int(recipes_limit)],
                many=True,
            ).data
        return RecipeShortenedSerializer(
            recipes,
            many=True,
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
