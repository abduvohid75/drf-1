from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Payments, Course
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='akkafzala@gmail.com',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('123password456')
        user.save()
