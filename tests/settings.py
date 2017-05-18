import os
import sys
import django


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

DEBUG = True

ADMINS = (
    ('admin', 'admin@location'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

ROOT_URLCONF = 'tests.url'

SITE_ID = 1

MEDIA_ROOT = ''

MEDIA_URL = ''

SECRET_KEY = '#($gm0!3&=yy^-3aka=0#y#2b1i$qn51tc$vpmplum1_$az8-='

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tests.urls'

if django.VERSION >= (1, 10):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'OPTIONS': {
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
                'debug': DEBUG,
            },
        }
    ]
else:
    TEMPLATE_DEBUG = DEBUG
    TEMPLATE_DIRS = (
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'notification',
    'notification.tests',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEST_RUNNER = 'notification.tests.compatibility.TestRunner'

