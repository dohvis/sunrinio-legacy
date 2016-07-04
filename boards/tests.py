from django.test import Client, TestCase

from accounts.models import User
from accounts.tests import make_user
from tags.models import Tag
from .models import Board, Post


def create_boards():
    names = ['스마트 틴 앱 챌린지', '모바일 콘텐츠 경진대회']
    boards = [(Board.objects.create(name=b)) for b in names]
    return boards


def write_post(boards=None):
    if boards is None:
        boards = create_boards()
    tags = Tag.objects.all()[:3] or [(Tag.objects.create(name=tag)) for tag in ['Python', '학교생활', 'JavaScript']]
    posts = (
        (boards[0], '제목1', User.objects.first(), '내용', tags),
    )
    for post in posts:
        Post.objects.create(board=post[0], title=post[1], author=post[2])
        Post.objects.create(board=post[0], title=post[1], author=post[2])


def board_init():
    boards = create_boards()
    write_post(boards=boards)


class TestBoardListAPI(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)
        create_boards()

    def test_listing(self):
        url = '/api/boards/'
        resp = self.c.get(url)

        self.assertJSONEqual(
            str(resp.content, encoding='utf8'),
            [
                {'name': '스마트 틴 앱 챌린지', 'pk': 1, 'posts': []},
                {'name': '모바일 콘텐츠 경진대회', 'pk': 2, 'posts': []},
            ]
        )


class TestBoardPostAPI(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)
        board_init()

    def test_listing(self):
        url = '/api/boards/?pk=1'
        resp = self.c.get(url)

        self.assertJSONEqual(
            str(resp.content, encoding='utf8'),
            [
                {
                    'name': '스마트 틴 앱 챌린지', 'pk': 1,
                    'posts': ['http://testserver/api/posts/1/', 'http://testserver/api/posts/2/'],
                },
            ]
        )


"""
class TestPostListAPI(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)
        board_init()

    def test_listing(self):
        get_cases = (
            (
                '',
                ({'messages': ''}),
            )
        )
        url = '/api/boards/1/?page=4'
        url = '/api/boards/1/hash-pk/'

    def test_writing(self):
        post_cases = (
            (
                '',
            )
        )

    def test_editing(self):
        pass

    def test_deleting(self):
        pass
"""
