# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0002_auto_20160507_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Want2Join',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=512, help_text='팀에게 남길 말을 간단히 작성해 주세요.')),
                ('team', models.ForeignKey(related_name='want2join', to='teams.Team')),
                ('user', models.ForeignKey(related_name='want2join', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
