from django.db import models
from django.contrib.auth.models import User


class Commit(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commit"
        verbose_name_plural = "Commits"
