from django.db import models


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
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MiningSpot(models.Model):
    body = models.ForeignKey(CelestialBody, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    materials = models.ManyToManyField(Material, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
