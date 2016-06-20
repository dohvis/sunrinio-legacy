from django.db import models
from accounts.models import User


class Dinner(models.Model):
    class Status:
        NEW = 1
        DEALING = 2
        SOLD_OUT = 3
        CHOICES = (
            (NEW, '판매 중'),
            (DEALING, '거래 중'),
            (SOLD_OUT, '판매 완료'),
        )

    seller = models.OneToOneField(User, related_name='dinners')
    date = models.DateField(auto_now=True)
    buyer_candidate = models.OneToOneField(User, null=True, related_name='buying_dinner')
    # When this is not NULL, then there's a buyer waiting
    price = models.IntegerField()
    message = models.CharField(max_length=128, help_text='구매자가 판매자에게 남길 메세지')
    status = models.IntegerField(choices=Status.CHOICES, default=Status.NEW, help_text='판매 완료 여부')

    def add_buyer(self, user):
        # Push an alert by doing something like
        # alert.PushAlert(self.seller, "%s wants to buy your dinner meal!"%(user))
        if isinstance(user, User):
            self.buyer_candidate = user

    def __str__(self):
        return "판매자:{}, 구매자:{}".format(self.seller, self.buyer_candidate)
