from datetime import datetime
from json import dumps
from django.test import Client, TestCase

from accounts.models import User
from accounts.tests import make_user
from dinner.models import Dinner


class TestModel(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', email='seller@gmail.com', grade=1, klass=2, number=3)
        self.buyer = User.objects.create_user(username='buyer', email='buyer@gmail.com', grade=2, klass=2, number=3)

    def test_selling(self):
        price = 1000
        s = Dinner.objects.create(seller=self.seller, buyer_candidate=self.buyer, price=price)
        self.assertEqual(s.price, price)


class TestDeal(TestCase):
    def setUp(self):
        self.user = make_user()
        self.c = Client()
        self.c.login(username=self.user.username, password='qwer1234')

    def _bringout_dinner(self):
        price = 1000
        res = self.c.post('/api/dinners/', data={'price': price})
        self.assertEqual(res.status_code, 201)

    def _buy_dinner(self):
        res = self.c.get('/api/dinners/')
        dinner_list = str(res.content, encoding='utf8')
        self.assertJSONEqual(
            dinner_list,
            [
                {
                    'seller': self.user.pk,
                    'price': 1000,
                    'status': 1,
                    'date': str(datetime.now().date())
                    # TODO: res['date'], Is it needed?
                },
            ]
        )
        self.assertEqual(res.status_code, 200)
        dinners = Dinner.objects.all()
        self.assertEqual(dinners.count(), 1)
        self.assertEqual(dinners.first().status, Dinner.Status.NEW)
        res = self.c.put(
            '/api/dinners/1/',
            data=dumps({'message': '2교시 끝나고 3-2로 갈께요', 'status': '2'}),
            status=Dinner.Status.DEALING,
            # TODO: res['status'], Is it needed?
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(dinners.first().status, Dinner.Status.DEALING)

    def _get_dinners(self):
        self._bringout_dinner()
        res = self.c.get('/api/dinners/')
        dinner_list = str(res.content, encoding='utf8')
        self.assertJSONEqual(
            dinner_list,
            [
                {
                    'seller': self.user.pk,
                    'price': 1000,
                    'status': 1,
                    'date': str(datetime.now().date())
                    # TODO: res['date'], Is it needed?
                },
            ]
        )
        self.assertEqual(res.status_code, 200)
        dinners = Dinner.objects.all()
        self.assertEqual(dinners.count(), 1)
        self.assertEqual(dinners.first().status, Dinner.Status.NEW)

    def test_get_dinners(self):
        self._get_dinners()

    def test_bringout_dinner(self):
        self._bringout_dinner()

    def test_invalid_buy_dinner(self):
        self._bringout_dinner()
        res = self.c.put(
            '/api/dinners/1/',
            data=dumps({'message': '2교시 끝나고 3-2로 갈께요', 'status': '2', 'price': 5000}),
            # TODO: res['status'], Is it needed?
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 200)
        dinner = Dinner.objects.first()
        self.assertEqual(dinner.status, Dinner.Status.DEALING)
        self.assertEqual(dinner.price, 1000)

    def test_buy_dinner(self):
        self._bringout_dinner()
        self._buy_dinner()

    def test_buy_dinner_accept(self):
        self._bringout_dinner()
        self._buy_dinner()
        dinners = Dinner.objects.all()
        self.assertEqual(dinners.first().status, Dinner.Status.DEALING)
        res = self.c.put(
            '/api/dinners/1/',
            data=dumps({'status': '3'}),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(dinners.count(), 1)
        self.assertEqual(dinners.first().status, Dinner.Status.SOLD_OUT)

    def test_buy_dinner_deny(self):
        self._bringout_dinner()
        self._buy_dinner()
        dinners = Dinner.objects.all()
        self.assertEqual(dinners.first().status, Dinner.Status.DEALING)
        res = self.c.put(
            '/api/dinners/1/',
            data=dumps({'status': '1'}),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 200)
        dinners = Dinner.objects.all()
        self.assertEqual(dinners.count(), 1)
        self.assertEqual(dinners.first().status, Dinner.Status.NEW)
