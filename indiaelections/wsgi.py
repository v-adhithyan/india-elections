"""
WSGI config for indiaelections project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "indiaelections.settings")

load_dotenv()
DEV_STATIC = os.environ["DEV_STATIC"]

if DEV_STATIC:
    application = Cling(get_wsgi_application())
else:
    application = get_wsgi_application()
