#encoding: utf-8
from django.conf import settings

PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 'plugshop.showcase.models.Product')