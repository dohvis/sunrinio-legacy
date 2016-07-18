from django.db import models
from accounts.models import User


class Openchat(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
