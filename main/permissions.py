"""The signals module for the main app."""

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_custom_permissions(**kwargs):
    """Create custom permissions for the app."""
    content_type = ContentType.objects.get_for_model(Permission)

    Permission.objects.get_or_create(
        codename="can_restart_processes",
        name="Can restart processes",
        content_type=content_type,
    )

    Permission.objects.get_or_create(
        codename="can_flush_processes",
        name="Can flush processes",
        content_type=content_type,
    )

    Permission.objects.get_or_create(
        codename="can_kill_processes",
        name="Can kill processes",
        content_type=content_type,
    )
