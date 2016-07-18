import os
import sys
from getpass import getuser

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    username = getuser()
    settings_file = os.path.join(BASE_DIR, 'sunrinio', 'settings', 'local_{}.py'.format(username))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunrinio.settings.local_{}".format(username))

    from django.core.management import execute_from_command_line

    try:
        execute_from_command_line(sys.argv)
    except ImportError:
        os.environ['DJANGO_SETTINGS_MODULE'] = ''
        os.environ["DJANGO_SETTINGS_MODULE"] = "sunrinio.settings.production"
        import django
        django.setup()
        execute_from_command_line(sys.argv)
