from django.forms import ModelForm, ModelMultipleChoiceField
from django.db.models.functions import Lower
from .models import System, CelestialBody, MiningSpot, Material

class SystemForm(ModelForm):
    class Meta:
        model = System
        fields = ["name", "notes"]

class BodyForm(ModelForm):
    def __init__(self, *args, hide_relationship_fields=False, **kwargs):
        super().__init__(*args, **kwargs)
        if hide_relationship_fields:
            self.fields.pop("system", None)
            self.fields.pop("parent_body", None)

    class Meta:
        model = CelestialBody
        fields = ["name", "system", "parent_body", "notes"]

class MiningSpotForm(ModelForm):
    def __init__(self, *args, hide_relationship_fields=False, sort="importance", **kwargs):
        super().__init__(*args, **kwargs)

        # Hide relationship field
        if hide_relationship_fields:
            self.fields.pop("body", None)

        # Fix type checker
        field = self.fields["materials"]
        assert isinstance(field, ModelMultipleChoiceField)

        # Base queryset: only enabled materials
        qs = Material.objects.filter(is_enabled=True)

        # Sorting logic
        if sort == "value":
            qs = qs.order_by("-value", Lower("name"))
        elif sort == "name":
            qs = qs.order_by(Lower("name"))
        else:  # default: importance
            qs = qs.order_by("-importance", Lower("name"))

        field.queryset = qs

        # Group materials by category for the template
        self.metals = field.queryset.filter(category="metal")
        self.minerals = field.queryset.filter(category="mineral")

    class Meta:
        model = MiningSpot
        # metals = Material.objects.filter(category="metal", is_enabled=True)
        # minerals = Material.objects.filter(category="mineral", is_enabled=True)

        fields = ["name", "body", "materials", "notes"]
