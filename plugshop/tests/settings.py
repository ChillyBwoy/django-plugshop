import os

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  ':memory',
    },
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
SECRET_KEY = '_uobce43e5osp8xgzle*yag2_16%y$sf*5(12vfg25hpnxik_*'
INSTALLED_APPS = [
    'django.contrib.auth',
    'plugshop',
    'tests',
]

DEBUG = True
TEMPLATE_DEBUG = DEBUG