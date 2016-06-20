from django.db import models

from accounts.models import User


class Meal(models.Model):
    class Type:
        LUNCH = 0
        DINNER = 1

    type = models.IntegerField(choices=Type, help_text='중식/석식')
    content = models.TextField(blank=False, default='급식이 제공되지 않습니다.', help_text='급식 내용')
    date = models.DateField(help_text='날짜')

    def __str__(self):
        return "{} {} {}".format("중식" if self.type == 0 else "석식", self.date, self.content)


class Review(models.Model):
    writer = models.ForeignKey(User, help_text='작성자')
    meal = models.ForeignKey(Meal, help_text='급식')
    rate = models.FloatField(default=0.0, help_text='평점')
    content = models.TextField(blank=False, help_text='후기')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}".format(self.meal, self.writer, self.rate)
