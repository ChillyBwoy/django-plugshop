import os

SECRET_KEY = '662hghj_$4ng_6tw!6aa!b&j7*jz55)5gzc&h5g4bdjr)g-05j'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'plugshop',
    'sample_shop',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

PLUGSHOP_MODELS = {
    'Product': 'sample_shop.Product',
}