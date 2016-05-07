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
            name='SellingItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(auto_now=True)),
                ('price', models.IntegerField()),
                ('buyer_candidate', models.OneToOneField(related_name='buying_dinner', null=True, to=settings.AUTH_USER_MODEL)),
                ('seller', models.OneToOneField(related_name='selling_dinner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
