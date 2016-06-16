from json import dumps
from django.test import Client, TestCase

from accounts.models import User
from tags.models import Tag
from scripts.init_data import create_tags


def make_user(login=False):
    username = 'testuser'
    password = 'qwer1234'
    user = User.objects.create_user(username=username, password=password, name='김선린', email='test@test.com',
                                    introduction='접대롤 잘함 / 스택하고파여',
                                    grade=1, klass=2, number=3)
    if login is True:
        client = Client()
        client.login(username=username, password=password)
        return user, client
    return user


def generate_image(name='test_image.png', width=10, height=10):
    from PIL import Image
    img = Image.new('RGB', (width, height))
    img.save(name)
    return name


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
        res = self.c.post('/api/auth/registration/', data=data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(User.objects.get(username=username).grade, grade)


class TestUpdateUserInfo(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)

    def _update_info(self, updated_data):
        url = '/api/users/{}/'.format(self.user.pk)
        res = self.c.patch(url, data=dumps(updated_data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.user.refresh_from_db()
        for key in updated_data.keys():
            obj_value = getattr(self.user, key)
            if obj_value != updated_data[key]:
                return False

        return True

    def test_update(self):
        updated_data = {"klass": 12, "number": 3}
        self.assertTrue(self._update_info(updated_data))

    def test_invalid_update(self):
        updated_data = {"email": "asdf"}
        self.assertFalse(self._update_info(updated_data))


class TestUserList(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)
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
                    "teams": [], "introduction": "접대롤 잘함 / 스택하고파여",
                    "profile_image": None,
                },
            ]
        )
