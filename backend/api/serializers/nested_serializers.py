from rest_framework import serializers

from api.models import Recipe


class RecipeShortenedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
