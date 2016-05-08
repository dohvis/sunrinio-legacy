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
    user = User.objects.create_user(username='testuser', password='qwer1234', email='test@gmail.com', grade=1, klass=2, number=3)
    return team, user


class TestModel(TestCase):
    def setUp(self):
        self.team, self.user = make_team_and_user()

    def test_add_member(self):
        self.team.member.add(self.user)
        self.assertEqual(self.team.member.all().count(), 1)


class TestJoinRequest(TestCase):
    def setUp(self):
        self.l_username = 'leader'
        self.l_pw = 'qwer1234'
        self.team_leader = User.objects.create_user(
            username=self.l_username,
            email='leader@gmail.com',
            password=self.l_pw,
            grade=2,
            klass=2,
            number=3
        )
        self.team, self.user = make_team_and_user()
        self.team.member.add(self.team_leader)
        self.c = Client()
        self.c.login(username=self.user.username, password='qwer1234')

    def test_join_request(self):
        res = self.c.post('/teams/{team_id}/want2join/'.format(team_id=self.team.id))
        self.assertEqual(res.status_code, 200)

        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'status': 'success'}
        )
        w = Want2Join.objects.first()
        self.assertEqual(w.team, self.team)
        self.assertEqual(w.user, self.user)
