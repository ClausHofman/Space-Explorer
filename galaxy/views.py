from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from .models import System, CelestialBody, MiningSpot

def system_list(request):
    systems = System.objects.all().order_by("name")
    return render(request, "galaxy/system_list.html", {"systems": systems})

def system_detail(request, pk):
    system = get_object_or_404(System, pk=pk)
    bodies = CelestialBody.objects.filter(system=system, parent_body__isnull=True).order_by("name")
    return render(request, "galaxy/system_detail.html", {
        "system": system,
        "bodies": bodies,
    })

def body_detail(request, pk):
    body = get_object_or_404(CelestialBody, pk=pk)

    # Moons = child bodies
    moons = CelestialBody.objects.filter(parent_body=body).order_by("name")

    # Mining spots on this body
    mining_spots = MiningSpot.objects.filter(body=body).order_by("name")

    return render(request, "galaxy/body_detail.html", {
        "body": body,
        "moons": moons,
        "mining_spots": mining_spots,
    })

def mining_spot_detail(request, pk):
    spot = get_object_or_404(MiningSpot, pk=pk)
    materials = spot.materials.all().order_by("name")

    return render(request, "galaxy/mining_spot_detail.html", {
        "spot": spot,
        "materials": materials,
    })

# Add system
class SystemForm(ModelForm):
    class Meta:
        model = System
        fields = ["name", "notes"]

def system_create(request):
    if request.method == "POST":
        form = SystemForm(request.POST)
        if form.is_valid():
            system = form.save()
            return redirect("system_detail", pk=system.pk)
    else:
        form = SystemForm()
    
    return render(request, "galaxy/system_form.html", {
        "form": form,
        "mode": "create",
    })


# Edit system
def system_edit(request, pk):
    system = get_object_or_404(System, pk=pk)

    if request.method == "POST":
        form = SystemForm(request.POST, instance=system)
        if form.is_valid():
            form.save()
            return redirect("system_detail", pk=system.pk)
    else:
        form = SystemForm(instance=system)

    return render(request, "galaxy/system_form.html", {
        "form": form,
        "mode": "edit",
    })


# Delete system
def system_delete(request, pk):
    system = get_object_or_404(System, pk=pk)

    if request.method == "POST":
        system.delete()
        return redirect("system_list")

    return render(request, "galaxy/system_confirm_delete.html", {"system": system})
