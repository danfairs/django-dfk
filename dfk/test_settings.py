# Django settings for foo project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dfk.db',
    }
}

ROOT_URLCONF = 'test_urls'

INSTALLED_APPS = (
    'dfk',
)

SECRET_KEY = '0af=nmwyehxzkzwmkd_zu$gq!+786d4g3-t3!ggtuc=$7lisey'
