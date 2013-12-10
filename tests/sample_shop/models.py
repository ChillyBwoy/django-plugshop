# -*- coding: utf-8 -*-

import datetime

from django.db import models

from plugshop.models import ProductAbstract


class Product(ProductAbstract):
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1)