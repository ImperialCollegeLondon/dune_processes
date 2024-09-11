"""Urls module for the main app."""

from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("restart/<uuid:uuid>", views.restart_process, name="restart"),
    path("kill/<uuid:uuid>", views.kill_process, name="kill"),
    path("flush/<uuid:uuid>", views.flush_process, name="flush"),
    path("logs/<uuid:uuid>", views.logs, name="logs"),
]
