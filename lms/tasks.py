from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from lms.models import Subscription


@shared_task
def email_update_course(course_id):
    """Send email to user if course was updated more than 4 hours."""

    subscription = Subscription.objects.filter(course_id=course_id)

    for sub in subscription:
        if sub.course.updated_at < timezone.now() + timezone.timedelta(hours=4):
            send_mail(
                subject="Обновление курса",
                message=f"Курс {sub.course.title} был обновлен",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[sub.user.email],
            )
