"""
WSGI config for sunrinseed project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import site
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

site.addsitedir('/home/nero/.virtualenvs/sseed/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunrinseed.settings")

application = get_wsgi_application()
