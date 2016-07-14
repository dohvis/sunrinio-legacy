from django.db import models


class Party(models.Model):
    name = models.CharField(max_length=32, help_text='학생회 이름(두드림,신명,청사진)', unique=True)

    def __str__(self):
        return self.name


class Promise(models.Model):
    party = models.ForeignKey(Party, related_name='promises')
    title = models.CharField(max_length=64, help_text='공약명')
    description = models.CharField(max_length=256, help_text='공약에 대한 설명')

    def __str__(self):
        return "{} {}".format(self.title, self.activity)


class Activity(models.Model):
    promise = models.ForeignKey(Promise, related_name='activities')
    image = models.ImageField(blank=True)
    content = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.promise.title, self.content)
