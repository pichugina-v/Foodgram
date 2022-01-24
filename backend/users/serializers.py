from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User, Follow
from api.models import Recipe


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
        if (user.id is not None and Follow.objects.filter(
                user=self.context['request'].user, author=obj
                ).exists()):
            return True
        return False


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
        if Follow.objects.filter(user=user, author=obj).exists():
            return True
        return False

    def get_recipes(self, obj):
        from api.serializers import RecipeShortenedSerializer
        recipes = Recipe.objects.filter(author=obj)
        return RecipeShortenedSerializer(
            recipes,
            many=True,
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
