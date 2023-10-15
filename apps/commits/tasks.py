from celery import shared_task
from django.contrib.auth.models import User

from .models import Commit


@shared_task
def create_daily_commit():
    for user in User.objects.all():
        Commit.objects.create(
            user=user,
            body="",
            bonus=0,
        )
