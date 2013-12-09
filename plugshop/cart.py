# -*- coding: utf-8 -*-

from django.utils import simplejson as json

from plugshop import settings
from plugshop.utils import serialize_model
from plugshop.signals import cart_append, cart_remove, cart_empty, cart_save


class CartStorage(object):
    pass


class CartItem(object):

    def __init__(self, product, price=0, quantity=1):
        self._product = product
        self._price = price
        self._quantity = quantity

    @property
    def price(self):
        return self._price * self._quantity


class Cart(object):

    def __init__(self, storage, name):
        self.storage = storage
        self.name = name
        self.goods = []

        for item, price, quantity in storage.get(self.name, []):
            self.append(item, price, quantity)

    def __iter__(self):
        return iter(self.goods)

    def __len__(self): 
        return len(self.goods)
        
    def total(self):
        return (sum(c.quantity for c in self.goods), 
                sum(p.price for p in self.goods))

    def _get_product(self, product):
        try:
            return filter(lambda x: x.product.pk == product.pk, self.goods)[0]
        except IndexError:
            return None

    def has_product(self, product):
        return self._get_product(product) or False

    def save(self):
        self.storage[self.name] = tuple(
            (item.product, item.price, item.quantity) for item in self.goods)
    
    def add(self, product, price=0, quantity=1):
        item = self._get_product(product)
        if item:
            self.goods[self.index(item)].quantity += quantity
    
    def remove(self, product, quantity=None):
        item = self._get_product(product)
        if item and quantity and item.quantity > quantity:
            self[self.index(item)].quantity -= quantity

    def empty(self):
        self.goods = []
    
    # def serialize(self):
    #     data = {
    #         'products': self.get_products(),
    #         'price_total': self.price_total(),
    #         'goods_total': len(self)
    #     }
    #     return data
    # 
    # def get_products(self):
    # 
    #     return [{'product': serialize_model(item.product),
    #             'price': item.price,
    #             'price_total': item.price_total(),
    #             'quantity': item.quantity} for item in self.goods]


def get_cart(request):
    return getattr(request, settings.REQUEST_NAMESPACE, None)