"""Urls module for the main app."""

from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
]
