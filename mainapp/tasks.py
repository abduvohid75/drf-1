from datetime import timezone

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from mainapp.models import Course
from users.models import User


@shared_task
def send_update_notification():
    courses = Course.objects.filter(is_changed=True)

    subject = "Обновление курса"
    from_email = "sendinfoforauth@gmail.com"

    for course in courses:
        subscribers = course.subs.split()
        message = render_to_string("email/update_notification.html", {"course": course})

        for subscriber in subscribers:
            send_mail(subject, message, from_email, [subscriber])
        course.is_changed = False
        course.save()

@shared_task
def check_and_block_inactive_users():
    current_time = timezone.now()
    one_month_ago = current_time - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)