"""
WSGI config for wiki project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.insert(0, os.path.abspath(root_path))
sys.path.insert(0, os.path.abspath(os.path.join(root_path, 'wiki')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
