from rest_framework import serializers

from .models import Tag, Ingridient, IngridientAmount, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fielda = ('__all__')


class IngridientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingridient'
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
            'id', 'name',
            'ingridient', 'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('__all__')
