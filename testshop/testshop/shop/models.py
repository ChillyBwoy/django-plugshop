# encoding: utf-8
import datetime
from django.db import models
from django.utils.translation import ugettext as _

from plugshop.models import ProductAbstract, CategoryAbstract

class Product(ProductAbstract):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True, 
                                                default=datetime.datetime.now)
    sort = models.PositiveIntegerField(blank=True, null=True, default=1)

class Category(CategoryAbstract):
    description = models.TextField(blank=True)
