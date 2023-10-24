from decimal import Decimal
from unittest import TestCase

from django.urls import reverse

from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

from rest_framework import status
from rest_framework.test import APIClient


RECIPES_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "Sample recipe",
        "time_minutes": 22,
        "price": Decimal("5.25"),
        "description": "Sample recipe description",
        "link": "http://example.com",
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)
    return recipe


class RecipeApiTests(TestCase):
    """Test recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe()
        create_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get the recipe detail"""
        recipe = create_recipe()

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            "title": "sample recipe",
            "time_minutes": 30,
            "price": Decimal("5.99"),
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_partial_update(self):
        """Test partial update of a recipe"""
        original_link = "https://example.com/recipe.pdf"
        recipe = create_recipe(
            title="Simple recipe title",
            link=original_link,
        )

        payload = {"title": "New recipe title"}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)

    def test_full_update(self):
        recipe = create_recipe(
            title="Simple recipe title",
            link="https://example.com/recipe.pdf",
            description="Simple recipe description",
        )

        payload = {
            "title": "New recipe title",
            "link": "https://example.com/new-recipe.pdf",
            "description": "New recipe description",
            "time_minutes": 20,
            "price": Decimal("2.50"),
        }

        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
