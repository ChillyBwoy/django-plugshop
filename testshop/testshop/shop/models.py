# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

from plugshop.models import ProductAbstract, ShippingAbstract, \
ShippingTypeAbstract, CategoryAbstract

class Product(ProductAbstract):
    doc = models.TextField(_(u'doc'), blank=True, null=True)

class ShippingType(ShippingTypeAbstract):
    help = models.TextField(_(u'подсказка'), blank=True, null=True)

class Category(CategoryAbstract):
    description = models.TextField(blank=True)

class Shipping(ShippingAbstract):
    phone = models.CharField(_(u'Телефон'), blank=True, null=True, 
                                max_length=80)
