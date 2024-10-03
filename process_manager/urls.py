"""Urls module for the process_manager app."""

from django.urls import include, path

from .views import actions, pages, partials

app_name = "process_manager"

partial_urlpatterns = [
    path("process_table/", partials.process_table, name="process_table"),
]

urlpatterns = [
    path("", pages.index, name="index"),
    path("process_action/", actions.process_action, name="process_action"),
    path("logs/<uuid:uuid>", pages.logs, name="logs"),
    path("boot_process/", pages.BootProcessView.as_view(), name="boot_process"),
    path("partials/", include(partial_urlpatterns)),
]
