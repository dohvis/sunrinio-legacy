"""
WSGI config for sunrinseed project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import site
from django.core.wsgi import get_wsgi_application

site.addsitedir('/home/nero/.virtualenvs/sseed/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunrinseed.settings")

application = get_wsgi_application()
