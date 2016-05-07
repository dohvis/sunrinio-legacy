# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.CharField(max_length=64, null=True, blank=True, help_text='이메일 주소')),
                ('is_staff', models.BooleanField(default=False, help_text='관리자 여부')),
                ('name', models.CharField(max_length=10, help_text='이름')),
                ('birthday', models.DateField(null=True, blank=True, help_text='생일')),
                ('addr', models.CharField(max_length=255, null=True, blank=True, help_text='주소')),
                ('entrance_year', models.IntegerField(help_text='입학년도')),
                ('grade', models.PositiveSmallIntegerField(help_text='학년')),
                ('klass', models.PositiveSmallIntegerField(help_text='반')),
                ('number', models.PositiveSmallIntegerField(help_text='번호')),
                ('graduate_year', models.IntegerField(help_text='졸업년도')),
                ('gender', models.IntegerField(choices=[(1, '남자'), (2, '여자')], null=True, blank=True, help_text='성별')),
                ('profile_image', models.ImageField(upload_to='profile_image')),
                ('introduction', models.CharField(max_length=256)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', related_name='user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64, help_text='ex) 스택/생활/게임/안드로이드앱/웹/Python/Django 등')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=models.ManyToManyField(to='accounts.Tag', related_name='users', help_text='유저 태그'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', to='auth.Permission', related_name='user_set', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
