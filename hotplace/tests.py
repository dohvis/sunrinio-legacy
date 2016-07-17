from django.test import TestCase
from django.utils.timezone import now
from accounts.tests import make_user
from hotplace.models import (
    Place,
    Review,
)


class TestPlace(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)

    def test_signal(self):
        place = Place.objects.create(name="노래방", x=126.96694811560961, y=37.544515649066426)
        Review.objects.create(place=place, user=self.user, rate=3.5, comment='asdf', when=now())
        Review.objects.create(place=place, user=self.user, rate=4.5, comment='asdf2', when=now())
        place.refresh_from_db()
        self.assertEqual(place.rate_avg, 4.0)

    def test_gps_filter(self):
        from sunrinseed.settings.base import STATICFILES_DIRS
        fp = open(STATICFILES_DIRS[0] + '/images/logo.png', "rb")
        excluded_place = {
            'x': 120.0, 'y': 37.0,
            'name': '육쌈냉면', 'description': '냉면에 고기싸줌', 'address': "서울특별시 용산구 청파동 111-58 ",
            'rate_avg': 5.0, 'url': 'http://testserver/api/places/1/', 'reviews': [],
            'telephone': '010-1234-5678',
        }
        included_place = {
            'x': 127.1, 'y': 37.0,
            'name': '육쌈냉면', 'description': '냉면에 고기싸줌', 'address': "서울특별시 용산구 청파동 111-58 ",
            'rate_avg': 5.0, 'url': 'http://testserver/api/places/2/', 'reviews': [], 'pk': 2,
            'telephone': '010-1234-5678',
        }
        for place in [excluded_place, included_place]:
            Place.objects.create(
                x=place['x'],
                y=place['y'],
                telephone=place['telephone'],
                name=place['name'],
                address=place['address'],
                rate_avg=place['rate_avg'],
                description=place['description'],
            )
        get_cases = (
            (
                {'ne': '43.0,132.0', 'sw': '32.0,124.0'},  # request
                (
                    200,
                    [included_place, ]
                ),  # response
            ),  # valid request
            (
                {'ne': '4.3,13.2', 'sw': '3.2,12.4'},
                (
                    200, []
                ),
            ),  # invalid request
        )
        url = '/api/places/'
        for case in get_cases:
            req_except = case[0]
            resp_except = case[1]
            resp = self.c.get(url, data=req_except)
            self.assertEqual(resp.status_code, resp_except[0])
            self.assertJSONEqual(str(resp.content, encoding='utf8'), resp_except[1])
