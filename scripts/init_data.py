from django.contrib.sites.models import Site
from django.core.files import File
from django.db.utils import (
    IntegrityError,
)
from accounts.models import Tag, User
from boards.models import (
    Board,
    Post,
)
from hotplace.models import Image, Place, Review
from allauth.socialaccount.models import SocialApp

FB_ID = "528049860707304"
FB_SECRET = "92cb5cd475a48d9aafec759a9e540e11"


def create_super_user():
    return User.objects.create_superuser(
        username='admin', email='a@gmail.com', password='qwer1234',
        grade=4, klass=1, number=1)


def create_tags():
    tag_list = ['python', 'django', 'flask', 'java', 'android', '모콘', 'STAC', 'APPJAM', 'nodejs']
    for tag in tag_list:
        Tag.objects.create(name=tag)
    return tag_list


def create_social_apps():
    fb = SocialApp.objects.create(provider='facebook', name='sunrinio', client_id=FB_ID, secret=FB_SECRET)
    fb.sites.add(Site.objects.first())
    fb.save()


def create_places():
    import pickle
    info_list = pickle.load("fixtures/near_sunrin.json")
    for info in info_list:
        Place.objects.create(
            name=info['name'],
            address=info['address'],
            telephone=info['telephone'],
            x=info['x'],
            y=info['y'],
        )
    return Place.objects.first()


def create_reviews():
    place = Place.objects.first() or create_places()
    place2 = Place.objects.all()[1]
    user = User.objects.first() or create_super_user()
    from sunrinseed.settings.base import BASE_DIR
    import os
    sulsam = open(os.path.join(BASE_DIR, 'media', 'sulsam.jpg'), 'rb')
    yuksam = open(os.path.join(BASE_DIR, 'media', '6sam.jpg'), 'rb')
    info_list = [
        ((place, user, 4, '좋아염'), [yuksam, ],),
        ((place2, user, 4, '좋아염'), [sulsam, ],),
    ]
    for info in info_list:
        review_info = info[0]
        review = Review.objects.create(
            place=review_info[0],
            user=review_info[1],
            rate=review_info[2],
            comment=review_info[3],
        )
        for img in info[1]:
            Image.objects.create(image=File(img), review=review)
    sulsam.close()
    yuksam.close()


def create_board():
    names = ['공지사항', '질문게시판']
    boards = [Board.objects.create(name=name) for name in names]
    return boards


def create_post():
    user = User.objects.first()
    board = Board.objects.first()
    tag = Tag.objects.first()
    p = Post.objects.create(board=board, title='제목', author=user)
    p.tags.add(tag)
    p.save()
    return p


def create_schedule():
    from datetime import date
    from schedule.models import Schedule
    schedules = [
        ("학급회장, 학생회장 선거", date(2016, 7, 15)),
        ("교내 해킹방어대회", date(2016, 7, 15)),
        ("꽃동네 봉사활동(1학년 멀티)", date(2016, 7, 19)),
    ]
    objs = [Schedule.objects.create(name=s[0], date=s[1]) for s in schedules]
    return objs


def create_council():
    from council.models import (
        Activity,
        Party,
        Promise,
    )
    parties = ("두드림", "신명", "청사진",)
    promises = [["Lotto Day", "빌려 Dream"], ["유니버셜 신명", "급식의 지니"], ["청사진 신문", "월단 청문회"], ]
    activities = [[], ["러브액츄얼리틀어줬읍니다", "오늘 급식에 연어나옴"], [], ]
    for party in parties:
        party = Party.objects.create(name=party)
        for promise in promises:
            promise = Promise.objects.create(party=party, title=promise)
            for activity in activities:
                Activity.objects.create(promise=promise, content=activity)


def run():
    try:
        create_social_apps()
        create_tags()
        print("[+] Create Tags")
    except IntegrityError:
        pass

    try:
        create_places()
        create_reviews()
        print("[+] Create Places and Reviews")

    except IntegrityError as e:
        print(e)

    try:
        create_super_user()
        print("[+] Create admin:qwer1234")
    except IntegrityError:
        pass

    try:
        create_board()
        create_post()
        print("[+] Create Board and Post")

    except IntegrityError as e:
        print(e)

    create_schedule()
    print("[+] Create Schedule")

    try:
        create_council()
        print("[+] Create Council")

    except IntegrityError as e:
        print(e)
