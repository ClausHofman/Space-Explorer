from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import SystemForm, BodyForm, MiningSpotForm, BodyCommentForm, MiningSpotCommentForm
from .models import System, CelestialBody, MiningSpot, BodyComment, MiningSpotComment


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
    bodies = CelestialBody.objects.filter(system=system)

    action_panel = panel_context(
        actions=[
            panel_action("Edit", reverse("system_edit", args=[system.pk])),
            panel_action("Delete", reverse("system_delete", args=[system.pk]), "delete"),
        ],
        add_items=[
            panel_add_item("Add Body", reverse("body_create_for_system", args=[system.pk])),
        ],
    )

    # Navbar
    spots = MiningSpot.objects.filter(body__system=system)

    comments = (
        BodyComment.objects.filter(body__system=system).count() +
        MiningSpotComment.objects.filter(spot__body__system=system).count()
    )

    navbar_items = [
        {"label": "Bodies", "count": bodies.count(), "url": reverse("system_bodies", args=[system.pk])},
        {"label": "Mining Spots", "count": spots.count(), "url": reverse("system_mining_spots", args=[system.pk])},
        {"label": "Comments", "count": comments, "url": reverse("system_comments", args=[system.pk])},
    ]


    return render(
        request,
        "galaxy/system_detail.html",
        {
            "system": system,
            "bodies": bodies,
            **action_panel,
            "navbar_items": navbar_items,
        }
    )


def body_detail(request, pk):
    body = get_object_or_404(CelestialBody, pk=pk)
    moons = CelestialBody.objects.filter(parent_body=body)
    spots = MiningSpot.objects.filter(body=body)

    action_panel = panel_context(
        actions=[
            panel_action("Edit", reverse("body_edit", args=[body.pk])),
            panel_action("Delete", reverse("body_delete", args=[body.pk]), "delete"),
        ],
        add_items=[
            panel_add_item("Add Moon", reverse("body_create_child", args=[body.pk])),
            panel_add_item("Add Mining Spot", reverse("mining_spot_create_for_body", args=[body.pk])),
            panel_add_item("Add Comment", reverse("body_comment_create", args=[body.pk])),
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

    action_panel = panel_context(
        actions=[
            panel_action("Edit", reverse("mining_spot_edit", args=[spot.pk])),
            panel_action("Delete", reverse("mining_spot_delete", args=[spot.pk]), "delete"),
        ],
        add_items=[
            panel_action("Add Comment", reverse("mining_spot_comment_create", args=[spot.pk])),
        ],
    )

    return render(request, "galaxy/mining_spot_detail.html", {
        "spot": spot,
        "materials": materials,
        **action_panel,
    })


# System
def system_create(request):
    cancel_url = reverse("system_list")

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
    cancel_url = reverse("system_detail", args=[system.pk])

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
    cancel_url = reverse("system_detail", args=[system.pk])

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
    cancel_url = reverse("body_detail", args=[body.pk])

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
    cancel_url = reverse("body_detail", args=[body.pk])

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
    cancel_url = reverse("system_detail", args=[system.pk])

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
    cancel_url = reverse("body_detail", args=[parent.pk])

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


# Mining spot
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


def mining_spot_edit(request, spot_pk):
    spot = get_object_or_404(MiningSpot, pk=spot_pk)
    cancel_url = reverse("mining_spot_detail", args=[spot.pk])
    selected_ids = set(spot.materials.values_list("id", flat=True))

    sort = request.GET.get("sort") or request.session.get("material_sort", "importance")
    request.session["material_sort"] = sort

    if request.method == "POST":
        form = MiningSpotForm(request.POST, instance=spot, hide_relationship_fields=True, sort=sort)
        if form.is_valid():
            form.save()
            return redirect("mining_spot_detail", pk=spot.pk)
    else:
        form = MiningSpotForm(instance=spot, hide_relationship_fields=True, sort=sort)

    return render(request, "galaxy/mining_spot_form.html", {
        "form": form,
        "mode": "edit",
        "cancel_url": cancel_url,
        "sort": sort,
        "selected_ids": selected_ids,
    })


def mining_spot_delete(request, pk):
    spot = get_object_or_404(MiningSpot, pk=pk)
    cancel_url = reverse("mining_spot_detail", args=[spot.pk])

    if request.method == "POST":
        spot_pk = spot.body.system.pk
        spot.delete()
        return redirect("body_detail", pk=spot.body.pk)

    return render(request, "galaxy/mining_spot_confirm_delete.html", {
        "mining_spot": spot,
        "cancel_url": cancel_url,
    })

# Comments
def body_comment_create(request, body_pk):
    body = get_object_or_404(CelestialBody, pk=body_pk)

    if request.method == "POST":
        form = BodyCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.body = body
            comment.save()
            return redirect("body_detail", pk=body.pk)
    else:
        form = BodyCommentForm()

    return render(request, "galaxy/comment_form.html", {
        "form": form,
        "target": body,
        "mode": "add",
    })

def mining_spot_comment_create(request, spot_pk):
    spot = get_object_or_404(MiningSpot, pk=spot_pk)

    if request.method == "POST":
        form = MiningSpotCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.spot = spot
            comment.save()
            return redirect("mining_spot_detail", pk=spot.pk)
    else:
        form = MiningSpotCommentForm()

    return render(request, "galaxy/comment_form.html", {
        "form": form,
        "target": spot,
        "mode": "add",
    })

def body_comment_edit(request, pk):
    comment = get_object_or_404(BodyComment, pk=pk)
    body = comment.body

    if request.method == "POST":
        form = BodyCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("body_detail", pk=body.pk)
    else:
        form = BodyCommentForm(instance=comment)

    return render(request, "galaxy/comment_form.html", {
        "form": form,
        "target": body,
        "mode": "edit",
    })

def body_comment_delete(request, pk):
    comment = get_object_or_404(BodyComment, pk=pk)
    body = comment.body

    if request.method == "POST":
        comment.delete()
        return redirect("body_detail", pk=body.pk)

    return render(request, "galaxy/comment_confirm_delete.html", {
        "comment": comment,
        "target": body,
    })

def mining_spot_comment_edit(request, pk):
    comment = get_object_or_404(MiningSpotComment, pk=pk)
    spot = comment.spot

    if request.method == "POST":
        form = MiningSpotCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("mining_spot_detail", pk=spot.pk)
    else:
        form = MiningSpotCommentForm(instance=comment)

    return render(request, "galaxy/comment_form.html", {
        "form": form,
        "target": spot,
        "mode": "edit",
    })

def mining_spot_comment_delete(request, pk):
    comment = get_object_or_404(MiningSpotComment, pk=pk)
    spot = comment.spot

    if request.method == "POST":
        comment.delete()
        return redirect("mining_spot_detail", pk=spot.pk)

    return render(request, "galaxy/comment_confirm_delete.html", {
        "comment": comment,
        "target": spot,
    })

# For navbar
def system_bodies(request, pk):
    system = get_object_or_404(System, pk=pk)
    bodies = CelestialBody.objects.filter(system=system)
    # bodies = system.bodies.all() # type: ignore[attr-defined]
    return render(request, "galaxy/system_bodies.html", {"system": system, "bodies": bodies})

def system_mining_spots(request, pk):
    system = get_object_or_404(System, pk=pk)
    spots = MiningSpot.objects.filter(body__system=system)
    return render(request, "galaxy/system_mining_spots.html", {"system": system, "spots": spots})

def system_comments(request, pk):
    system = get_object_or_404(System, pk=pk)

    # Comments on bodies in this system
    body_comments = BodyComment.objects.filter(body__system=system)

    # Comments on mining spots in this system
    spot_comments = MiningSpotComment.objects.filter(spot__body__system=system)

    # Combine and sort by created_at descending
    comments = sorted(
        list(body_comments) + list(spot_comments),
        key=lambda c: c.created_at,
        reverse=True
    )

    return render(request, "galaxy/system_comments.html", {
        "system": system,
        "comments": comments,
    })
