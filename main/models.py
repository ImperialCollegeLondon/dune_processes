"""Models module for the main app."""

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models  # noqa: F401


class User(AbstractUser):
    """Custom user model for this project."""

    class Meta:
        """Meta class for the User model."""

        permissions: ClassVar = [
            ("can_restart_processes", "Can restart processes"),
            ("can_flush_processes", "Can flush processes"),
            ("can_kill_processes", "Can kill processes"),
        ]
