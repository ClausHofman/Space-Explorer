from django.urls import path
from . import views

urlpatterns = [
    path("systems/", views.system_list, name="system_list"),
    path("systems/<int:pk>/", views.system_detail, name="system_detail"),
    path("bodies/<int:pk>/", views.body_detail, name="body_detail"),
    path("mining-spots/<int:pk>/", views.mining_spot_detail, name="mining_spot_detail"),
    path("", views.system_list, name="home"),

    # Add, edit, delete system
    path("systems/add/", views.system_create, name="system_create"),
    path("systems/<int:pk>/edit/", views.system_edit, name="system_edit"),
    path("systems/<int:pk>/delete/", views.system_delete, name="system_delete"),

]
