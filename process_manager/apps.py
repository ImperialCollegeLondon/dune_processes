"""Apps module for the process_manager app."""

from django.apps import AppConfig


class ProcessManagerConfig(AppConfig):
    """The app config for the process_manager app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "process_manager"
