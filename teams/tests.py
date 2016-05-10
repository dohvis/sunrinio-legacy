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
    user = User.objects.create_user(username='testuser', password='qwer1234', email='test@gmail.com', grade=1, klass=2,
                                    number=3)
    team_leader = User.objects.create_user(
        username='leader',
        email='leader@gmail.com',
        password='qwer1234',
        grade=2,
        klass=2,
        number=3
    )
    team.members.add(team_leader)
    return team, team_leader, user


class TestModel(TestCase):
    def setUp(self):
        self.team, self.leader, self.user = make_team_and_user()

    def test_add_member(self):
        self.team.members.add(self.user)
        self.assertEqual(self.team.members.all().count(), 2)


class TestTeamList(TestCase):
    def setUp(self):
        self.team, self.leader, self.user = make_team_and_user()
        self.c = Client()
        self.c.login(username=self.user.username, password='qwer1234')

    def test_team_list_view(self):
        res = self.c.get('/api/teams/')
        self.assertEqual(res.status_code, 200)
        print(res.content)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            [
                {
                    'tags': [],
                    'url': 'http://testserver/api/teams/1/',
                    'name': '테스트팀',
                    'users': ['http://testserver/api/users/2/'],
                    'introduce': '스택나가요',
                    'content': '이거이거 만들꺼고 우린 이런사람이고 디자이너필요함요'
                },
            ]
        )


class TestJoinRequest(TestCase):
    def setUp(self):
        self.l_username = 'leader'
        self.l_pw = 'qwer1234'

        self.team, self.leader, self.user = make_team_and_user()
        self.c = Client()
        self.c.login(username=self.user.username, password='qwer1234')

    def test_join_request(self):
        res = self.c.post('/team/{team_id}/want2join/'.format(team_id=self.team.id))
        self.assertEqual(res.status_code, 200)

        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'status': 'success'}
        )
        w = Want2Join.objects.first()
        self.assertEqual(w.team, self.team)
        self.assertEqual(w.user, self.user)
