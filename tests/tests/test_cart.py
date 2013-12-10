# -*- coding: utf-8 -*-

from django.test import TestCase

from plugshop.cart import Cart
from sample_shop.models import Product


class CartTest(TestCase):
    
    def setUp(self):
        self.product1 = Product.objects.get(slug='brief-history-time')
        self.product2 = Product.objects.get(slug='programming-python')
        self.product3 = Product.objects.get(slug='dive-python')
        self.product4 = Product.objects.get(slug='1984-new-classic-edition')
        
        self.storage = {
            'test_cart': (
                (self.product1, self.product1.price, 1),
                (self.product2, self.product2.price, 2),
                (self.product3, self.product3.price, 1),
            )
        }
        
    def test_cart_iteration(self):
        cart = Cart(self.storage, 'test_cart')
        for product, price, quantity in cart:
            pass
            
    def test_cart_add(self):
        cart = Cart(self.storage, 'test_cart')
        cart.add(self.product4, self.product4.price)
        cart.add(self.product4, self.product4.price)
        
        for product, price, quantity in cart:
            # print product, price, quantity
            pass
        
    
    def test_cart_remove(self):
        cart = Cart(self.storage, 'test_cart')
        
        print '*' * 100
        print cart.total_quantity, cart.total_price
        cart.remove(self.product2, 1)
        print cart.total_quantity, cart.total_price        
    