# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='ex) 스택/생활/게임/안드로이드앱/웹/Python/Django 등', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='팀 이름', max_length=64)),
                ('introduce', models.CharField(help_text='팀 소개', max_length=512)),
                ('content', models.TextField(help_text='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('member', models.ManyToManyField(help_text='팀원', to=settings.AUTH_USER_MODEL, related_name='teams')),
                ('tags', models.ManyToManyField(to='teams.Tag', related_name='teams')),
            ],
        ),
    ]
