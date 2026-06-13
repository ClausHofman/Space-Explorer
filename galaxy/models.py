from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class System(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CelestialBody(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="bodies")
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

    def get_absolute_url(self):
        return reverse("body_detail", args=[self.pk])


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
    body = models.ForeignKey(CelestialBody, on_delete=models.CASCADE, related_name="mining_spots")
    name = models.CharField(max_length=200)
    materials = models.ManyToManyField(Material, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mining_spot_detail", args=[self.pk])

class BodyComment(models.Model):
    body = models.ForeignKey(CelestialBody, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.body.name}"

class MiningSpotComment(models.Model):
    spot = models.ForeignKey(MiningSpot, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.spot.name}"
