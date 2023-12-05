from django.db import models


class Recipe(models.Model):
    """Recipe object"""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField("Ingredient")

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """Ingredient for recipes"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
