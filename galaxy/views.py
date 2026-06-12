from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import SystemForm, BodyForm, MiningSpotForm
from .models import System, CelestialBody, MiningSpot


def panel_action(label, url, css_class=""):
    return {"label": label, "url": url, "class": css_class}


def panel_add_item(label, url):
    return {"label": label, "url": url}


def panel_context(actions=None, add_items=None):
    return {
        "actions": actions or [],
        "add_items": add_items or [],
    }


def resolve_cancel_url(request, fallback_url):
    return (
        request.POST.get("next")
        or request.GET.get("next")
        or request.META.get("HTTP_REFERER")
        or fallback_url
    )

def system_list(request):
    systems = System.objects.all().order_by("name")

    action_panel = panel_context(
        add_items=[
            panel_add_item("Add System", reverse("system_create")),
        ]
    )

    return render(
        request,
        "galaxy/system_list.html",
        {
            "systems": systems,
            **action_panel,
        }
    )


def system_detail(request, pk):
    system = get_object_or_404(System, pk=pk)
    bodies = CelestialBody.objects.filter(system=system, parent_body__isnull=True)

    action_panel = panel_context(
        actions=[
            panel_action("Edit System", reverse("system_edit", args=[system.pk])),
            panel_action("Delete System", reverse("system_delete", args=[system.pk]), "delete"),
        ],
        add_items=[
            panel_add_item("Add Body", reverse("body_create_for_system", args=[system.pk])),
        ],
    )

    return render(
        request,
        "galaxy/system_detail.html",
        {
            "system": system,
            "bodies": bodies,
            **action_panel,
        }
    )


def body_detail(request, pk):
    body = get_object_or_404(CelestialBody, pk=pk)
    moons = CelestialBody.objects.filter(parent_body=body)
    spots = MiningSpot.objects.filter(body=body)

    action_panel = panel_context(
        actions=[
            panel_action("Edit Body", reverse("body_edit", args=[body.pk])),
            panel_action("Delete Body", reverse("body_delete", args=[body.pk]), "delete"),
        ],
        add_items=[
            panel_add_item("Add Moon", reverse("body_create_child", args=[body.pk])),
            panel_add_item("Add Mining Spot", reverse("mining_spot_create_for_body", args=[body.pk])),
        ],
    )

    return render(
        request,
        "galaxy/body_detail.html",
        {
            "body": body,
            "moons": moons,
            "spots": spots,
            **action_panel,
        }
    )


def mining_spot_detail(request, pk):
    spot = get_object_or_404(MiningSpot, pk=pk)
    materials = spot.materials.all().order_by("name")

    return render(request, "galaxy/mining_spot_detail.html", {
        "spot": spot,
        "materials": materials,
    })


# System
def system_create(request):
    fallback_url = reverse("system_list")
    cancel_url = resolve_cancel_url(request, fallback_url)

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
        "cancel_url": cancel_url,
    })


def system_edit(request, pk):
    system = get_object_or_404(System, pk=pk)
    fallback_url = reverse("system_detail", args=[system.pk])
    cancel_url = resolve_cancel_url(request, fallback_url)

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
        "cancel_url": cancel_url,
    })


def system_delete(request, pk):
    system = get_object_or_404(System, pk=pk)
    fallback_url = reverse("system_detail", args=[system.pk])
    cancel_url = resolve_cancel_url(request, fallback_url)

    if request.method == "POST":
        system.delete()
        return redirect("system_list")

    return render(request, "galaxy/system_confirm_delete.html", {
        "system": system,
        "cancel_url": cancel_url,
    })


# Bodies
def body_edit(request, pk):
    body = get_object_or_404(CelestialBody, pk=pk)
    fallback_url = reverse("body_detail", args=[body.pk])
    cancel_url = resolve_cancel_url(request, fallback_url)

    if request.method == "POST":
        form = BodyForm(request.POST, instance=body, hide_relationship_fields=True)
        if form.is_valid():
            form.save()
            return redirect("body_detail", pk=body.pk)
    else:
        form = BodyForm(instance=body, hide_relationship_fields=True)

    return render(request, "galaxy/body_form.html", {
        "form": form,
        "mode": "edit",
        "cancel_url": cancel_url,
    })


def body_delete(request, pk):
    body = get_object_or_404(CelestialBody, pk=pk)
    fallback_url = reverse("body_detail", args=[body.pk])
    cancel_url = resolve_cancel_url(request, fallback_url)

    if request.method == "POST":
        system_pk = body.system.pk
        body.delete()
        return redirect("system_detail", pk=system_pk)

    return render(request, "galaxy/body_confirm_delete.html", {
        "body": body,
        "cancel_url": cancel_url,
    })


def body_create_for_system(request, system_pk):
    system = get_object_or_404(System, pk=system_pk)
    fallback_url = reverse("system_detail", args=[system.pk])
    cancel_url = resolve_cancel_url(request, fallback_url)

    if request.method == "POST":
        form = BodyForm(request.POST, hide_relationship_fields=True)
        if form.is_valid():
            body = form.save(commit=False)
            body.system = system
            body.parent_body = None
            body.save()
            return redirect("body_detail", pk=body.pk)
    else:
        form = BodyForm(hide_relationship_fields=True)

    return render(request, "galaxy/body_form.html", {
        "form": form,
        "mode": "add",
        "cancel_url": cancel_url,
    })


def body_create_child(request, parent_pk):
    parent = get_object_or_404(CelestialBody, pk=parent_pk)
    fallback_url = reverse("body_detail", args=[parent.pk])
    cancel_url = resolve_cancel_url(request, fallback_url)

    if request.method == "POST":
        form = BodyForm(request.POST, hide_relationship_fields=True)
        if form.is_valid():
            body = form.save(commit=False)
            body.system = parent.system
            body.parent_body = parent
            body.save()
            return redirect("body_detail", pk=body.pk)
    else:
        form = BodyForm(hide_relationship_fields=True)

    return render(request, "galaxy/body_form.html", {
        "form": form,
        "mode": "add",
        "cancel_url": cancel_url,
    })


def mining_spot_create_for_body(request, body_pk):
    body = get_object_or_404(CelestialBody, pk=body_pk)
    cancel_url = reverse("body_detail", args=[body.pk])

    sort = request.GET.get("sort") or request.session.get("material_sort", "importance")

    # Save sorting to session
    request.session["material_sort"] = sort

    if request.method == "POST":
        form = MiningSpotForm(
            request.POST,
            hide_relationship_fields=True,
            sort=sort)
        if form.is_valid():
            spot = form.save(commit=False)
            spot.body = body
            spot.save()
            return redirect("mining_spot_detail", pk=spot.pk)
    else:
        form = MiningSpotForm(initial={"body": body}, hide_relationship_fields=True, sort=sort)

    return render(request, "galaxy/mining_spot_form.html", {
        "form": form,
        "mode": "add",
        "cancel_url": cancel_url,
        "sort": sort,
    })
