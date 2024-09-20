"""The apps module for the main app."""

from django.apps import AppConfig


class MainConfig(AppConfig):
    """The app config for the main app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self) -> None:
        """Import permissions to ensure they are registered."""
        import main.permissions  # noqa: F401
