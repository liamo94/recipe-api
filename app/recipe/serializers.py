from rest_framework import serializers

from core.models import Recipe, Ingredient
from recipe.service import RecipeService


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""

    ingredients = IngredientSerializer(many=True, required=False)
    recipeService = RecipeService()

    class Meta:
        model = Recipe
        fields = ["id", "title", "ingredients"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a recipe"""
        return self.recipeService.create(validated_data)

    def update(self, instance, validated_data):
        return self.recipeService.update(instance, validated_data)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for the recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
