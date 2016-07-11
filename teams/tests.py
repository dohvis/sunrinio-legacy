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
    """
    팀 목록 조회 테스트
    """

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
    """
    팀 가입 요청 테스트
    """

    def setUp(self):
        self.l_username = 'leader'
        self.l_pw = 'qwer1234'

        self.team, self.leader, self.user = make_team_and_user()
        self.c = Client()
        self.c.login(username=self.user.username, password='qwer1234')

    def test_join_request(self):
        post_cases = (
            (
                {'base_url': "/api/teams/{team_pk}/join/", 'pk': self.team.pk, "params": {'message': "껴주세요"}},
                {'status_code': 201, 'data': {'message': '가입신청 되었습니다. 결과를 기다려 주세요.'}},
                True
            ),
            (
                {'base_url': "/api/teams/{team_pk}/join/", 'pk': self.team.pk + 1, "params": {'message': "껴주세요"}},
                {'status_code': 404, 'data': {'detail': 'Not found.'}},
                False
            ),
        )
        for case in post_cases:
            request, response, is_valid = case
            url = request['base_url'].format(team_pk=request['pk'])
            res = self.c.post(url, data=request['params'])
            self.assertEqual(res.status_code, response['status_code'])

            self.assertJSONEqual(
                str(res.content, encoding='utf8'),
                response['data']
            )
            try:
                w = Want2Join.objects.get(pk=request['pk'])
            except Want2Join.DoesNotExist:
                continue
            self.assertEqual(w.team == self.team, is_valid)
            self.assertEqual(w.user == self.user, is_valid)
            self.assertEqual(w.message == "껴주세요", is_valid)
