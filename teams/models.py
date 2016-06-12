from django.db import models

from accounts.models import User
from tags.models import Tag


class Team(models.Model):
    name = models.CharField(max_length=64, help_text='팀 이름')
    introduce = models.CharField(max_length=512, help_text='팀 소개')
    tags = models.ManyToManyField(Tag, related_name='teams')
    content = models.TextField(help_text='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, related_name='teams', help_text='팀원')

    @property
    def users(self):
        return self.members

    def __str__(self):
        return '<%s>' % self.name


class Want2Join(models.Model):
    team = models.ForeignKey(Team, related_name='want2join')
    user = models.ForeignKey(User, related_name='want2join')
    message = models.CharField(max_length=512, help_text='팀에게 남길 말을 간단히 작성해 주세요.')

    def __str__(self):
        return '<%s 가 %s에 들어가기를 희망합니다>' % (self.user.username, self.team.name)
