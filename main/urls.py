"""Urls module for the main app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("restart/<str:uuid>/", views.restart_process, name="restart"),
]
