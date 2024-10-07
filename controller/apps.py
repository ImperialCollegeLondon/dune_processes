"""Apps module for the controller app."""

from django.apps import AppConfig


class ControllerConfig(AppConfig):
    """The app config for the controller app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "controller"
