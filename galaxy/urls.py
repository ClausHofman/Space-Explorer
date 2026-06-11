from django.urls import path
from . import views

urlpatterns = [
    path("systems/", views.system_list, name="system_list"),
    path("systems/<int:pk>/", views.system_detail, name="system_detail"),
    path("bodies/<int:pk>/", views.body_detail, name="body_detail"),
    path("mining-spots/<int:pk>/", views.mining_spot_detail, name="mining_spot_detail"),
    path("", views.system_list, name="home"),

    # System list URLs
    path("systems/add/", views.system_create, name="system_create"),
    path("systems/<int:pk>/edit/", views.system_edit, name="system_edit"),
    path("systems/<int:pk>/delete/", views.system_delete, name="system_delete"),

    # System detail URLs
    path("bodies/<int:pk>/edit/", views.body_edit, name="body_edit"),
    path("bodies/<int:pk>/delete/", views.body_delete, name="body_delete"),
    path("systems/<int:system_pk>/bodies/add/", views.body_create_for_system, name="body_create_for_system"),
    path("bodies/<int:parent_pk>/add/", views.body_create_child, name="body_create_child"),

    # Body detail URLs
    path("bodies/<int:body_pk>/mining-spots/add/", views.mining_spot_create_for_body, name="mining_spot_create_for_body"),
]
