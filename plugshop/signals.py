# -*- coding: utf-8 -*-

from django.dispatch import Signal

cart_append = Signal(providing_args=['item', 'price', 'quantity'])
cart_remove = Signal(providing_args=['item', 'quantity'])
cart_empty = Signal()
cart_save = Signal()

order_create = Signal(providing_args=['order', 'request'])
