# coding: utf-8
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'debug_toolbar_mongo'

TEMPLATE_DIRS = (os.path.join(
    os.path.dirname(__file__), 'templates').replace('\\', '/'), )
INSTALLED_APPS = ('debug_toolbar_mongo', )
