from django.contrib import admin
from .models import System, CelestialBody, Material, MiningSpot


# Inline: Mining spots shown inside a CelestialBody page
class MiningSpotInline(admin.TabularInline):
    model = MiningSpot
    extra = 1


# Inline: Moons shown inside a CelestialBody page
class MoonInline(admin.TabularInline):
    model = CelestialBody
    fk_name = "parent_body"
    extra = 1


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(CelestialBody)
class CelestialBodyAdmin(admin.ModelAdmin):
    list_display = ("name", "system", "parent_body")
    list_filter = ("system",)
    search_fields = ("name",)
    inlines = [MoonInline, MiningSpotInline]
    ordering = ("system", "name")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "importance", "value", "is_enabled"]
    list_editable = ["importance", "value", "is_enabled"]
    list_filter = ["category", "is_enabled"]


@admin.register(MiningSpot)
class MiningSpotAdmin(admin.ModelAdmin):
    list_display = ("name", "body")
    list_filter = ("body__system",)
    search_fields = ("name", "notes")
    ordering = ("body", "name")
