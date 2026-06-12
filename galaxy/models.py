from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class System(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CelestialBody(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    parent_body = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="moons"
    )
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    CATEGORY_CHOICES = [
        ("metal", "Metal"),
        ("mineral", "Mineral"),
        ("gas", "Gas"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="metal")
    is_enabled = models.BooleanField(default=True)
    value = models.IntegerField(default=0)
    importance = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )

    def __str__(self):
        return self.name

class MiningSpot(models.Model):
    body = models.ForeignKey(CelestialBody, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    materials = models.ManyToManyField(Material, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
