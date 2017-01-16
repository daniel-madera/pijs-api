"""
WSGI config for pijs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pijs.settings")
os.environ['HTTPS'] = "on"
os.environ['wsgi.url_scheme'] = 'https'

application = get_wsgi_application()
