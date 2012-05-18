import time
from django.utils import simplejson as json

from plugshop import settings
from plugshop.utils import serialize_model


class CartItem(object):

    def __init__(self, product, price=0, quantity=1):
        self.product = product
        self.price = price
        self.quantity = quantity

    def price_total(self):
        return self.price * self.quantity

class Cart(list):

    def __init__(self, request, name):
        super(Cart, self).__init__()
        self.request = request
        self.name = name
        
        for item, price, quantity in request.session.get(self.name, []):
            self.append(item, price, quantity)

    def __len__(self): 
        return sum(c.quantity for c in self)

    def _get_product(self, product):
        try:
            return filter(lambda x: x.product.pk == product.pk, self)[0]
        except IndexError:
            return None
            
    def has_product(self, product):
        return self._get_product(product) or False

    def save(self):
        self.request.session[self.name] = tuple(
                (item.product, item.price, item.quantity) for item in self)
    
    def append(self, product, price=0, quantity=1):
        item = self._get_product(product)
        if item:
            self[self.index(item)].quantity += quantity
        else:
            super(Cart, self).append(
                CartItem(product, price, quantity)
            )
    
    def remove(self, product, quantity=None):
        item = self._get_product(product)
        if item:
            if quantity:
                if item.quantity > quantity:
                    self[self.index(item)].quantity -= quantity
                else:
                    super(Cart, self).remove(item)
            else:
                super(Cart, self).remove(item)

    def empty(self):
        while len(self):
            self.pop()

    def price_total(self):
        return sum([p.price_total() for p in self])
        
    def serialize(self):
        data = {
            'products': self.get_products(),
            'price_total': self.price_total(),
            'goods_total': len(self)
        }
        return data

    def get_products(self):
        return [{
                'product': serialize_model(item.product),
                'price': item.price,
                'price_total': item.price_total(),
                'quantity': item.quantity
            } for item in self]
                


def get_cart(request):
    return getattr(request, settings.REQUEST_NAMESPACE, None)
