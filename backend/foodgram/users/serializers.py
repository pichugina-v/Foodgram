from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
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
            'pk',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if Follow.objects.filter(user=user, author=obj).exists():
            return True
        return False


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'pk',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed'
        )

    def get_user_subscriptions():
        pass
