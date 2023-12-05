from core.models import Recipe, Ingredient

"""
For more complex data types/data types that diverge from the django models,
I would define some DTOs here.
"""


class RecipeService:
    """Recipe API service layer"""

    def _get_or_create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_obj, _ = Ingredient.objects.get_or_create(**ingredient)
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe"""
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
