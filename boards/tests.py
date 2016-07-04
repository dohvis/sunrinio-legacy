from django.test import Client, TestCase

from accounts.models import User
from accounts.tests import make_user
from tags.models import Tag
from .models import Board, Post


# TODO: 접근 제어 테스트

def create_boards():
    names = ['공지사항', '자유게시판']
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


def board_init():
    boards = create_boards()
    write_post(boards=boards)


class TestBoardAPI(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)
        board_init()

    def test_board(self):
        cases = (
            (
                '/api/boards/', [
                    {'name': '공지사항', 'id': 1, 'posts': ['http://testserver/api/posts/1/', ],},
                    {'name': '자유게시판', 'id': 2, 'posts': []},
                ],
            ),
            (
                '/api/boards/?pk=1', [
                    {
                        'name': '공지사항', 'id': 1,
                        'posts': ['http://testserver/api/posts/1/', ],
                    },
                ]
            )
        )
        for case in cases:
            resp = self.c.get(case[0])
            self.assertJSONEqual(str(resp.content, encoding='utf8'), case[1])


class TestPostAPI(TestCase):
    def setUp(self):
        username = 'testuser'
        password = 'qwer1234'
        User.objects.create_user(username=username, password=password, name='김선린', email='test@test.com',
                                 introduction='접대롤 잘함 / 스택하고파여',
                                 grade=1, klass=2, number=3)

        self.c = Client(enforce_csrf_checks=True)
        self.c.login(username=username, password=password)
        self.c.cookies['csrftoken'] = 'just' * 8
        board_init()

    def test_post(self):
        first_post = Post.objects.first()
        get_cases = (
            ('/api/posts/1/', {
                'author': 'test@test.com', 'board': '공지사항',
                'content': '',
                'id': 1,
                'tags': [],
                'title': '제목1',
                'created_at': first_post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': first_post.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }, 200),
        )

        for case in get_cases:
            resp = self.c.get(case[0])
            print(resp.content)
            self.assertEqual(resp.status_code, case[2])
            self.assertJSONEqual(str(resp.content, encoding='utf8'), case[1])

        post_cases = (
            ('/api/posts/', {'title': '제목', 'content': '내용', 'board': '공지사항', 'author': 'test@test.com'}, 201),
            ('/api/posts/', {'title': '제목', 'content': '내용', 'board': '1', 'author': 'test@test.com'}, 400),
        )

        for case in post_cases:
            params = case[1]
            params['csrfmiddlewaretoken'] = 'just' * 8
            resp = self.c.post(case[0], params)
            print(resp.content)
            self.assertEqual(resp.status_code, case[2])

        # TODO: 수정, 삭제 테스트
        """
        patch_cases = (
        )

        delete_cases = (
        )
        """


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
