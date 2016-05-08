from accounts.models import User


def run():
    User.objects.create_superuser(username='admin', email='a@gmail.com', password='qwer1234',
                                  grade=4, klass=1, number=1)
    print("[+] Create admin:qwer1234")
