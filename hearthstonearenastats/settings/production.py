import os

from hearthstonearenastats.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hearthstats',
        'USER': 'hearthdbuser',
        'PASSWORD': os.environ.get('DBPASS'),
        'HOST': 'localhost',
        'PORT': '',
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

TEMPLATE_DIRS = (
    '/webapps/hearthstonearenastats/templates',
)
