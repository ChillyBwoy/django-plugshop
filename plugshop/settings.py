#encoding: utf-8
from django.conf import settings

PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 'plugshop.defaults.Product')
#GROUP_MODEL = getattr(settings, 'PLUGSHOP_GROUP_MODEL', 'plugshop.defaults.ProductGroup')
