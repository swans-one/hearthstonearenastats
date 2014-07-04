import os

from hearthstonearenastats.settings.base import *   # noqa

project_root = os.path.abspath(os.path.dirname('__file__'))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testing.sqlitedb',
    },
}

TEMPLATE_DIRS = (
    os.path.join(project_root, 'templates'),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(9^m2^z@*h2yn1d266854b)6z6-6$h)*%cjfyit1kf0vcl!m29'


STATICFILES_DIRS = (
    os.path.join(project_root, 'static'),
)
