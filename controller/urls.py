"""Urls module for the controller app."""

from django.urls import path

from . import views

app_name = "controller"
urlpatterns = [
    path("", views.index, name="index"),
]
