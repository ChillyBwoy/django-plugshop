# encoding: utf-8
import datetime
from django.db import models
from django.utils.translation import ugettext as _

from plugshop.models import ProductAbstract, ShippingAbstract, \
ShippingTypeAbstract, CategoryAbstract

class Product(ProductAbstract):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True, 
                                                default=datetime.datetime.now)
    sort = models.PositiveIntegerField(blank=True, null=True, default=1)
    
class ShippingType(ShippingTypeAbstract):
    description = models.TextField(blank=True)

class Category(CategoryAbstract):
    description = models.TextField(blank=True)

class Shipping(ShippingAbstract):
    phone = models.CharField(_(u'Телефон'), blank=True, null=True, 
                                max_length=80)