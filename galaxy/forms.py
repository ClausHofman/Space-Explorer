from django.forms import ModelForm
from .models import System, CelestialBody, MiningSpot

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
    class Meta:
        model = MiningSpot
        fields = ["name", "body", "materials", "notes"]
