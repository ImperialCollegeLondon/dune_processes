"""Models module for the main app."""

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models  # noqa: F401


class User(AbstractUser):
    """Custom user model for this project."""

    class Meta:
        """Meta class for the User model."""

        permissions: ClassVar = [
            ("can_modify_processes", "Can modify processes"),
            ("can_view_process_logs", "Can view process logs"),
        ]
