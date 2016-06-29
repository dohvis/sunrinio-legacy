from django.test import TestCase


class TestPlace(TestCase):
    def setUp(self):
        pass

    def test_invalid_request(self):
        get_cases = (
            (
                {'x': 'aa', 'y': 'aa'},
                ('400',)
            ),
            ('post', {'x', 'y', }),
            ('put', {'', ''})
        )

    def test_valid_request(self):
        cases = (
            ('get', {'x': 1.0, 'y': 1.0}),
            ('post', {'x', 'y', }),
            ('put', {'', ''})
        )
