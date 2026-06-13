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

    # Mining spot detail URLs
    path("mining_spots/<int:spot_pk>/edit/", views.mining_spot_edit, name="mining_spot_edit"),
    path("mining_spots/<int:pk>/delete/", views.mining_spot_delete, name="mining_spot_delete"),

    # Comments
    path("bodies/<int:body_pk>/add-comment/", views.body_comment_create, name="body_comment_create"),
    path("mining-spots/<int:spot_pk>/add-comment/", views.mining_spot_comment_create, name="mining_spot_comment_create"),

    path("comments/body/<int:pk>/edit/", views.body_comment_edit, name="body_comment_edit"),
    path("comments/body/<int:pk>/delete/", views.body_comment_delete, name="body_comment_delete"),

    path("comments/spot/<int:pk>/edit/", views.mining_spot_comment_edit, name="mining_spot_comment_edit"),
    path("comments/spot/<int:pk>/delete/", views.mining_spot_comment_delete, name="mining_spot_comment_delete"),

    # Navbar
    path("systems/<int:pk>/bodies/", views.system_bodies, name="system_bodies"),
    path("systems/<int:pk>/spots/", views.system_mining_spots, name="system_mining_spots"),
    path("systems/<int:pk>/comments/", views.system_comments, name="system_comments"),


]
