from django.test import Client, TestCase

from accounts.models import User, Tag
from scripts.init_data import create_tags


def make_user():
    user = User.objects.create_user(username='testuser', password='qwer1234', name='김선린', email='test@test.com',
                                    introduction='접대롤 잘함 / 스택하고파여',
                                    grade=1, klass=2, number=3)
    return user


class UserTestCase(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_user_create(self):
        self.assertEqual(self.user.graduate_year, self.user.entrance_year + 2)


class TestAuthentication(TestCase):
    def setUp(self):
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


class TestUserList(TestCase):
    def setUp(self):
        self.user = make_user()
        self.c = Client()
        self.c.login(username='testuser', password='qwer1234')
        self.tags = create_tags()

        for tag_name in self.tags[:2]:
            tag = Tag.objects.get(name=tag_name)
            self.user.tags.add(tag)

    def test_user_list(self):
        res = self.c.get('/api/users/')
        self.assertEqual(res.status_code, 200)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            [
                {
                    "url": "http://testserver/api/users/1/", "username": "testuser", "name": "김선린",
                    "grade": 1, "klass": 2, "number": 3,
                    "tags": ['<python>', '<django>'],
                    "teams": [], "introduction": "접대롤 잘함 / 스택하고파여"
                },
            ]
        )
