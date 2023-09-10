from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Payments, Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        course = Course.objects.get(id=1)
        Payments.objects.create(
            user='Abc',
            date='2023-08-26 14:21:02.677708+00:00',
            course=course,
            sum_pay=1000,
            pay_met=True,
        )
        Payments.objects.create(
            user='Abcq',
            date='2023-08-26 14:21:02.677708+00:00',
            course=course,
            sum_pay=2000,
            pay_met=False,
        )