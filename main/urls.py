"""Urls module for the main app."""

from django.urls import include, path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
]
