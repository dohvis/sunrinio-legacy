from django.test import TestCase

from accounts.models import User


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', grade=1, klass=2, number=3)
        self.user = user

    def test_user_create(self):
        self.assertEqual(self.user.graduate_year, self.user.entrance_year + 2)
