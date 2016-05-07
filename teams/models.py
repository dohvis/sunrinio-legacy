from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, help_text='ex) 스택/생활/게임/안드로이드앱/웹/Python/Django 등')

    def __str__(self):
        return '<%s>' % self.name


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
