#----------------------------------------------------------------------
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------

"""
WSGI config for whyness_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://REMOVED
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.realpath(BASE_DIR))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whyness_django.settings')

application = get_wsgi_application()
