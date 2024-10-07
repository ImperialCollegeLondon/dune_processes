"""Urls module for the process_manager app."""

from django.urls import include, path

from . import views

app_name = "process_manager"

partial_urlpatterns = [
    path("process_table/", views.process_table, name="process_table"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("process_action/", views.process_action, name="process_action"),
    path("logs/<uuid:uuid>", views.logs, name="logs"),
    path("boot_process/", views.BootProcessView.as_view(), name="boot_process"),
    path("partials/", include(partial_urlpatterns)),
]
