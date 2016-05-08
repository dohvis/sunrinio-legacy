from django.test import Client, TestCase

from accounts.models import User


def make_user():
    user = User.objects.create_user(username='testuser', email='test@test.com', grade=1, klass=2, number=3)
    return user


class UserTestCase(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_user_create(self):
        self.assertEqual(self.user.graduate_year, self.user.entrance_year + 2)


class TestAuthentication(TestCase):
    def setUp(self):
        self.user = make_user()
        self.c = Client()

    def test_signup(self):
        username = 'signupuser'
        pw = 'password'
        grade = 1
        data = {'username': username, 'password1': pw, 'password2': pw, 'email': 'signupuser@gmail.com',
                'grade': grade, 'klass': 2, 'number': 3}
        res = self.c.post('/accounts/auth/registration/', data=data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(User.objects.get(username=username).grade, grade)
