# -*- coding: utf-8 -*-

from django.dispatch import Signal

cart_add = Signal(providing_args=['product', 'price', 'quantity'])
cart_remove = Signal(providing_args=['product', 'quantity'])
cart_empty = Signal()
cart_save = Signal()

order_create = Signal(providing_args=['order', 'request'])