# -*- coding: utf-8 -*-

import datetime

from django.db import models

from plugshop.models import ProductAbstract


class Product(ProductAbstract):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=1)