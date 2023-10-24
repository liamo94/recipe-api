from rest_framework import viewsets

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeDetailSerializer

    def get_queryset(self):
        """Retrieve recipes"""
        return self.queryset.order_by("-id")

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    # TODO: Do I need this?
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()
