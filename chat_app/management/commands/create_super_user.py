from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create a superuser with predefined credentials"

    def handle(self, *args, **kwargs):
        username = "admin"
        password = "password123"
        email = "admin@example.com"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, password=password, email=email
            )
            self.stdout.write(self.style.SUCCESS("Successfully created superuser"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
