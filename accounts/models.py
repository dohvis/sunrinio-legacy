from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, help_text='ex) 스택/생활/게임/안드로이드앱/웹/Python/Django 등')

    def __str__(self):
        return '<%s>' % self.name


class User(AbstractBaseUser, PermissionsMixin):
    class Gender:
        MALE = 1
        FEMALE = 2
        CHOICES = (
            (MALE, '남자'),
            (FEMALE, '여자'),
        )

    objects = UserManager()

    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=64, null=True, blank=True, help_text="이메일 주소")
    is_staff = models.BooleanField(default=False, help_text="관리자 여부")

    name = models.CharField(max_length=10, null=False, help_text="이름")
    birthday = models.DateField(blank=True, null=True, help_text="생일")
    addr = models.CharField(max_length=255, blank=True, null=True, help_text='주소')

    entrance_year = models.IntegerField(help_text="입학년도")
    grade = models.PositiveSmallIntegerField(help_text="학년")
    klass = models.PositiveSmallIntegerField(help_text="반")
    number = models.PositiveSmallIntegerField(help_text="번호")

    def get_default_graduate_year(self):
        return self.entrance_year+3

    graduate_year = models.IntegerField(help_text="졸업년도", default=get_default_graduate_year)
    gender = models.IntegerField(choices=Gender.CHOICES, null=True, blank=True, help_text='성별')

    profile_image = models.ImageField(upload_to='profile_image')
    introduction = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag, related_name='users', help_text="유저 태그")

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(self).__init__(*args, **kwargs)
        self._password = None

    def __str__(self):
        return '<User %s>' % self.user.username
