# -*- coding: utf-8 -*-

from collections import namedtuple
from django.utils import simplejson as json

from plugshop import settings
from plugshop.utils import serialize_model
from plugshop.signals import cart_add, cart_remove, cart_empty, cart_save


CartItem = namedtuple('CartItem', ['product', 'price', 'quantity'])



class Cart(object):

    def __init__(self, storage, name):
        self._storage = storage
        self._name = name
        self._goods = []
        self.restore()

    def __iter__(self):
        return iter(self._goods)

    def __len__(self): 
        return len(self._goods)
        
    def _get_product(self, product):
        try:
            return [p for p in self._goods if p.product is product][0]
        except IndexError:
            return None

    def add(self, product, price=0, quantity=1, **kwargs):
        item = self._get_product(product)
        if item:
            index = self._goods.index(item)
            cart_item = self._goods[index]
            self._goods[index] = CartItem(cart_item.product, cart_item.price, 
                                            cart_item.quantity + quantity)
        else:
            self._goods.append(CartItem(product, price, quantity))
        if not kwargs.pop('stop_signal', False):
            cart_add.send(sender=self, item=item or product, price=price, 
                            quantity=quantity)
    
    @property
    def total_quantity(self):
        return sum(p.quantity for p in self._goods)

    @property
    def total_price(self):
        return sum(p.price * p.quantity for p in self._goods)

    def has_product(self, product):
        return self._get_product(product) or False

    def save(self):
        self._storage[self._name] = tuple((item.product, item.price, 
                                        item.quantity) for item in self._goods)
        return self._storage
        
    def restore(self):
        for item, price, quantity in self._storage.get(self._name, []):
            self.add(item, price, quantity, stop_signal=True)

    def remove(self, product, quantity=0):
        item = self._get_product(product)
        if item:
            if quantity and item.quantity > quantity:
                index = self._goods.index(item)
                cart_item = self._goods[index]
                self._goods[index] = CartItem(cart_item.product, 
                                            cart_item.price, 
                                            cart_item.quantity - quantity)
            else:
                self._goods.remove(item)

    def empty(self):
        self._goods = []

def get_cart(request):
    return getattr(request, settings.REQUEST_NAMESPACE, None)