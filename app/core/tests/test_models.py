from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_recipe(self):
        recipe = models.Recipe.objects.create(
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Some recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)