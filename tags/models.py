from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text='ex) 스택/생활/게임/안드로이드앱/웹/Python/Django 등')

    def __str__(self):
        return '<%s>' % self.name
