from django.test import TestCase, Client
from accounts.models import User
from teams.models import (
    Team,
    Want2Join,
)


def make_team_and_user():
    team = Team.objects.create(
        name='테스트팀',
        introduce='스택나가요',
        content='이거이거 만들꺼고 우린 이런사람이고 디자이너필요함요'
    )
    user = User.objects.create_user(username='testuser', email='test@gmail.com', grade=1, klass=2, number=3)
    return team, user


class TestModel(TestCase):
    def setUp(self):
        self.team, self.user = make_team_and_user()

    def test_add_member(self):
        self.team.member.add(self.user)
        self.assertEqual(self.team.member.all().count(), 1)
