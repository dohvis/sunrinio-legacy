from django.test import TestCase

from accounts.models import User
from dinner.models import SellingItem


class TestModel(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', email='seller@gmail.com', grade=1, klass=2, number=3)
        self.buyer = User.objects.create_user(username='buyer', email='buyer@gmail.com', grade=2, klass=2, number=3)

    def test_selling(self):
        price = 1000
        s = SellingItem.objects.create(seller=self.seller, buyer_candidate=self.buyer, price=price)
        self.assertEqual(s.price, price)
