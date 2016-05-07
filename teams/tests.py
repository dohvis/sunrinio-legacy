from django.test import TestCase
from django.contrib.auth.models import User
from teams.models import (
    Tag,
    Team,
)


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='1234')
        self.team = Team.objects.create(
            name='테스트팀',
            introduce='스택나가요',
            content='이거이거 만들꺼고 우린 이런사람이고 디자이너필요함요'
        )

    def test_add_member(self):
        self.team.member.add(self.user)
        self.team.save()
        self.assertEqual(self.team.member.all().count(), 1)
