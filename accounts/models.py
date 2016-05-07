from django.contrib.auth.models import User
from django.db import models

from teams.models import Tag


class Profile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to='profile_image')
    description = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag, related_name='users')

    def __str__(self):
        return '<%s>' % self.user.username
