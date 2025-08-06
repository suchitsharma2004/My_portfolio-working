"""
WSGI config for MacOS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the settings module based on environment
if os.environ.get('VERCEL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MacOS.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MacOS.settings')

application = get_wsgi_application()

# Vercel expects the app to be available as a function
app = application
