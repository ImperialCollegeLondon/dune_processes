"""Urls module for the main app."""

from django.urls import include, path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("process_action/", views.process_action, name="process_action"),
    path("logs/<uuid:uuid>", views.logs, name="logs"),
    path("boot_process/", views.BootProcessView.as_view(), name="boot_process"),
]
