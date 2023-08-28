from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='superuser@superuser.net',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password('12345')
        user.save()
