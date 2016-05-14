from django.contrib.sites.models import Site
from accounts.models import Tag, User

from allauth.socialaccount.models import SocialApp

FB_ID = "528049860707304"
FB_SECRET = "92cb5cd475a48d9aafec759a9e540e11"


def create_tags():
    tag_list = ['python', 'django', 'flask', 'java', 'android', '모콘', 'STAC', 'APPJAM', 'nodejs']
    for tag in tag_list:
        Tag.objects.create(name=tag)
    return tag_list


def create_social_apps():
    fb = SocialApp.objects.create(provider='facebook', name='EduPick', client_id=FB_ID, secret=FB_SECRET)
    fb.sites.add(Site.objects.first())
    fb.save()


def run():
    create_social_apps()
    create_tags()
    print("[+] Create Tags")
    User.objects.create_superuser(username='admin', email='a@gmail.com', password='qwer1234',
                                  grade=4, klass=1, number=1)
    print("[+] Create admin:qwer1234")
