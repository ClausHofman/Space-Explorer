from django.shortcuts import render, get_object_or_404
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