"""The apps module for the main app."""

from django.apps import AppConfig


class MainConfig(AppConfig):
    """The app config for the main app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
