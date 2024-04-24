import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Command to create superuser."""

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@localhost",
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(os.getenv("ADMIN_PASSWORD"))
        user.save()
