from django.db import models
from django.contrib.auth.models import User


class SellingItem(models.Model):
    seller = models.OneToOneField(User, related_name='selling_dinner')
    date = models.DateField(auto_now=True)
    buyer_candidate = models.OneToOneField(User, null=True, related_name='buying_dinner')  # When this is not NULL, then there's a buyer waiting
    price = models.IntegerField()

    def add_buyer(self, user):
        # Push an alert by doing something like
        # alert.PushAlert(self.seller, "%s wants to buy your dinner meal!"%(user))
        if isinstance(user, User):
            self.buyer_candidate = user
