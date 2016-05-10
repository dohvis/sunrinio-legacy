from django.test import TestCase

from accounts.models import User
from dinner.models import Dinner


class TestModel(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', email='seller@gmail.com', grade=1, klass=2, number=3)
        self.buyer = User.objects.create_user(username='buyer', email='buyer@gmail.com', grade=2, klass=2, number=3)

    def test_dinner_create(self):
        price = 1000
        s = Dinner.objects.create(seller=self.seller, buyer_candidate=self.buyer, price=price)
        self.assertEqual(s.price, price)
