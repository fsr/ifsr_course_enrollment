#!/usr/bin/env python3
"""
WSGI config for cource manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cm_config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
