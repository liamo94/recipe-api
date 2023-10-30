from rest_framework import viewsets, mixins

from core.models import Ingredient, Recipe
from recipe import serializers
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "search",
                OpenApiTypes.STR,
                description="Fuzzy search of the recipe title",
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    serializer_class = serializers.RecipeDetailSerializer

    def get_queryset(self):
        """Return objects for authenticated user"""
        search = self.request.query_params.get("search")
        queryset = Recipe.objects.all()
        if search:
            queryset = queryset.filter(title__contains=search)

        return queryset.order_by("id").distinct()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class


class IngredientViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage ingredients in the database"""

    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Retrieve ingredients"""
        queryset = Ingredient.objects.all()
        return queryset.order_by("id").distinct()
