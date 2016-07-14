from django.test import TestCase
from accounts.tests import make_user
from council.models import (
    Activity,
    Party,
    Promise,
)


class CouncilTest(TestCase):
    def setUp(self):
        self.user, self.c = make_user(login=True)

    def test_council(self):
        party = Party.objects.create(name="두드림")
        promise = Promise.objects.create(party=party, title="공약1", description="설명")
        activity = Activity.objects.create(promise=promise, content="내용")
        get_cases = (
            (
                '/api/party/{}/promises/'.format(party.pk),
                [{
                    'party_name': party.name,
                    'title': promise.title,
                    'description': promise.description,
                    'activities': [
                        {
                            'content': activity.content,
                            'image': activity.image,
                            'created_at': activity.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            'updated_at': activity.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        },
                    ],
                },]
            ),
        )
        for case in get_cases:
            resp = self.c.get(case[0])
            self.assertEqual(resp.status_code, 200)
            self.assertJSONEqual(str(resp.content, encoding='utf8'), case[1])

        post_cases = (
            (
                '/api/council/sinmyung/',
                {'title': '공약명', 'description': '설명'}
            ),
            (
                '/api/council/sinmyung/1/',
                {'image': '증거사진', 'content': '내용'}
            ),
        )

        patch_cases = (
            (
                '/api/council/sinmyung/',
                {'pk': 1, 'description': '설명바뀜'}
            ),
            (
                '/api/council/sinmyung/1/',
                {'pk': 1, 'image': '증거사진 바뀜'}
            ),

        )
