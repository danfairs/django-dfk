# Django settings for foo project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dfk.db',                      # Or path to database file if using sqlite3.
    }
}

ROOT_URLCONF = 'test_urls'

INSTALLED_APPS = (
    'dfk',
)
