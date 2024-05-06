from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_activity_users(user_id):
    """Check activity users."""

    user = User.objects.get(id=user_id)

    if user.last_login < timezone.now() - timezone.timedelta(days=30):
        user.is_active = False
        user.save()
