from accounts.models import User, Tag
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=64, help_text='팀 이름')
    introduce = models.CharField(max_length=512, help_text='팀 소개')
    tags = models.ManyToManyField(Tag, related_name='teams')
    content = models.TextField(help_text='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ManyToManyField(User, related_name='teams', help_text='팀원')

    def __str__(self):
        return '<%s>' % self.name
