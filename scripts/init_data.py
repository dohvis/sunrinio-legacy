from accounts.models import Tag, User


def create_tags():
    tag_list = ['python', 'django', 'flask', 'java', 'android', '모콘', 'STAC', 'APPJAM', 'nodejs']
    for tag in tag_list:
        Tag.objects.create(name=tag)
    return tag_list


def run():
    create_tags()
    print("[+] Create Tags")
    User.objects.create_superuser(username='admin', email='a@gmail.com', password='qwer1234',
                                  grade=4, klass=1, number=1)
    print("[+] Create admin:qwer1234")
